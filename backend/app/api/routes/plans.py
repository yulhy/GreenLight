from fastapi import APIRouter, HTTPException

from app.repositories.catalog_repository import get_item
from app.schemas.plan import (
    AlternativePlan,
    CarbonBreakdown,
    CurrentPlanAnalysis,
    PlanAnalysisRequest,
    PlanAnalysisResponse,
)
from app.services.analyzer import (
    analyze_plan,
    calculate_category_percentages,
)
from app.services.calculator import calculate_item
from app.services.recommendation_service import (
    recommend_for_hotspots,
)


router = APIRouter(
    tags=["Plans"],
)


@router.post(
    "/plans/analyze",
    response_model=PlanAnalysisResponse,
    summary="행사 계획 탄소배출량 및 비용 분석",
)
async def analyze_plan_route(
    request: PlanAnalysisRequest,
) -> PlanAnalysisResponse:
    """
    사용자가 선택한 행사 계획을 분석한다.

    현재 단계:
    - 비용 데이터 계산 가능
    - 탄소계수 데이터가 없으면 탄소 관련 값은 None
    - 탄소 데이터가 있을 때만 hotspot / 친환경 대안 추천 수행
    """

    # =====================================================
    # 1. 현재 선택 항목 조회 및 계산
    # =====================================================

    calculated_items: list[dict] = []

    for selection in request.selections:
        catalog_item = get_item(
            category=selection.category,
            item_id=selection.itemId,
        )

        if catalog_item is None:
            raise HTTPException(
                status_code=404,
                detail=(
                    "카탈로그 항목을 찾을 수 없습니다: "
                    f"category={selection.category}, "
                    f"itemId={selection.itemId}"
                ),
            )

        try:
            calculated = calculate_item(
                item=catalog_item,
                quantity=selection.quantity,
            )

        except ValueError as exc:
            raise HTTPException(
                status_code=400,
                detail=str(exc),
            ) from exc

        calculated_items.append(
            calculated
        )

    if not calculated_items:
        raise HTTPException(
            status_code=400,
            detail="분석할 항목이 없습니다.",
        )

    # =====================================================
    # 2. 현재 계획 분석
    # =====================================================

    analysis = analyze_plan(
        calculated_items
    )

    category_breakdown = (
        calculate_category_percentages(
            analysis["categoryBreakdown"]
        )
    )

    current_plan = CurrentPlanAnalysis(
        totalCarbonKgCo2e=analysis[
            "totalCarbonKgCo2e"
        ],
        totalCostKrw=analysis[
            "totalCostKrw"
        ],
        breakdown=[
            CarbonBreakdown(
                category=item["category"],
                carbonKgCo2e=item.get(
                    "carbonKgCo2e"
                ),
                sharePercent=item.get(
                    "percentage"
                ),
            )
            for item in category_breakdown
        ],
    )

    # =====================================================
    # 3. 탄소 데이터 존재 여부 확인
    # =====================================================

    baseline_total_carbon = (
        float(
            analysis["totalCarbonKgCo2e"]
        )
        if analysis["totalCarbonKgCo2e"]
        is not None
        else None
    )

    baseline_total_cost = float(
        analysis["totalCostKrw"]
    )

    # =====================================================
    # 4. Hotspot 분석
    # =====================================================

    hotspots = analysis["hotspots"]

    hotspot_categories = [
        hotspot["category"]
        for hotspot in hotspots
    ]

    # =====================================================
    # 5. 대안 추천 생성
    # =====================================================

    preferences = request.preferences

    if baseline_total_carbon is not None:
        recommendation_candidates = (
            recommend_for_hotspots(
                calculated_items=calculated_items,
                hotspots=hotspots,
                budget_krw=request.budgetKrw,
                max_additional_cost_krw=(
                    preferences.maxAdditionalCostKrw
                ),
                avoid_items=(
                    preferences.avoidItems
                ),
            )
        )
    else:
        recommendation_candidates = []

    # =====================================================
    # 6. 대안을 전체 계획 기준으로 계산
    # =====================================================

    alternatives: list[AlternativePlan] = []

    if baseline_total_carbon is not None:
        for index, recommendation in enumerate(
            recommendation_candidates,
            start=1,
        ):
            baseline_item_carbon = float(
                recommendation[
                    "baselineCarbonKgCo2e"
                ]
            )

            alternative_item_carbon = float(
                recommendation[
                    "alternativeCarbonKgCo2e"
                ]
            )

            baseline_item_cost = float(
                recommendation[
                    "baselineCostKrw"
                ]
            )

            alternative_item_cost = float(
                recommendation[
                    "alternativeCostKrw"
                ]
            )

            # 기존 항목을 대안 항목으로 교체했을 때
            # 전체 탄소배출량 계산
            alternative_total_carbon = (
                baseline_total_carbon
                - baseline_item_carbon
                + alternative_item_carbon
            )

            # 기존 항목을 대안 항목으로 교체했을 때
            # 전체 비용 계산
            alternative_total_cost = (
                baseline_total_cost
                - baseline_item_cost
                + alternative_item_cost
            )

            if baseline_total_carbon == 0:
                reduction_percent = 0.0
            else:
                reduction_percent = (
                    (
                        baseline_total_carbon
                        - alternative_total_carbon
                    )
                    / baseline_total_carbon
                    * 100
                )

            alternative_id = (
                f"alt-{index}-"
                f"{recommendation['alternativeItemId']}"
            )

            alternatives.append(
                AlternativePlan(
                    id=alternative_id,
                    name=(
                        f"{recommendation['originalItem']} → "
                        f"{recommendation['alternativeItem']}"
                    ),
                    changedCategories=[
                        recommendation["category"]
                    ],
                    totalCarbonKgCo2e=(
                        alternative_total_carbon
                    ),
                    totalCostKrw=(
                        alternative_total_cost
                    ),
                    carbonReductionPercent=(
                        reduction_percent
                    ),
                    costDifferenceKrw=(
                        alternative_total_cost
                        - baseline_total_cost
                    ),
                    constraintsSatisfied=(
                        recommendation["feasible"]
                    ),
                )
            )

    # =====================================================
    # 7. 추천 대안 선택
    # =====================================================

    recommended = next(
        (
            alternative
            for alternative in alternatives
            if alternative.constraintsSatisfied
        ),
        None,
    )

    if baseline_total_carbon is None:
        recommended_alternative_id = None

        recommendation_reason = (
            "탄소배출계수 데이터가 아직 연결되지 않아 "
            "친환경 대안 추천을 생성할 수 없습니다."
        )

    elif recommended is not None:
        recommended_alternative_id = (
            recommended.id
        )

        recommendation_reason = (
            "사용자 조건을 만족하는 대안 중 "
            "탄소 감축 효과가 큰 대안을 선택했습니다."
        )

    elif alternatives:
        recommended_alternative_id = None

        recommendation_reason = (
            "탄소 감축 대안은 존재하지만 "
            "현재 사용자 조건을 모두 만족하는 "
            "대안을 찾지 못했습니다."
        )

    else:
        recommended_alternative_id = None

        recommendation_reason = (
            "현재 계획보다 탄소배출량을 줄일 수 있는 "
            "대안을 찾지 못했습니다."
        )

    # =====================================================
    # 8. 최종 응답
    # =====================================================

    return PlanAnalysisResponse(
        currentPlan=current_plan,
        hotspots=hotspot_categories,
        alternatives=alternatives,
        recommendedAlternativeId=(
            recommended_alternative_id
        ),
        recommendationReason=(
            recommendation_reason
        ),
        disclaimer=(
            "비용은 등록된 기준 데이터를 바탕으로 계산한 "
            "추정치입니다. 탄소배출계수 데이터가 없는 항목은 "
            "탄소배출량이 표시되지 않습니다."
        ),
    )