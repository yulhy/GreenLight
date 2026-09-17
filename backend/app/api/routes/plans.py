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
from app.services.recommendation_service import recommend_for_hotspots


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

    처리 과정:
    1. catalog에서 선택 항목 조회
    2. 항목별 탄소배출량 / 비용 계산
    3. 전체 계획 및 카테고리별 분석
    4. 탄소배출 hotspot 탐지
    5. hotspot 중심 대안 생성
    6. 사용자 조건에 맞는 추천 대안 선정
    """

    # -----------------------------------------------------
    # 1. 현재 선택 항목 계산
    # -----------------------------------------------------

    calculated_items = []

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

        calculated = calculate_item(
            item=catalog_item,
            quantity=selection.quantity,
        )

        calculated_items.append(calculated)

    # -----------------------------------------------------
    # 2. 현재 계획 분석
    # -----------------------------------------------------

    analysis = analyze_plan(
        calculated_items
    )

    category_breakdown = calculate_category_percentages(
        analysis["categoryBreakdown"]
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
                carbonKgCo2e=item[
                    "carbonKgCo2e"
                ],
                sharePercent=item[
                    "percentage"
                ],
            )
            for item in category_breakdown
        ],
    )

    # -----------------------------------------------------
    # 3. Hotspot
    # -----------------------------------------------------

    hotspots = analysis["hotspots"]

    hotspot_categories = [
        hotspot["category"]
        for hotspot in hotspots
    ]

    # -----------------------------------------------------
    # 4. 대안 생성
    # -----------------------------------------------------

    preferences = request.preferences

    recommendation_candidates = (
        recommend_for_hotspots(
            calculated_items=calculated_items,
            hotspots=hotspots,
            budget_krw=request.budgetKrw,
            max_additional_cost_krw=(
                preferences.maxAdditionalCostKrw
            ),
            avoid_items=preferences.avoidItems,
        )
    )

    # -----------------------------------------------------
    # 5. 대안을 전체 계획 기준 수치로 변환
    # -----------------------------------------------------

    alternatives: list[AlternativePlan] = []

    baseline_total_carbon = float(
        analysis["totalCarbonKgCo2e"]
    )

    baseline_total_cost = float(
        analysis["totalCostKrw"]
    )

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

        alternative_total_carbon = (
            baseline_total_carbon
            - baseline_item_carbon
            + alternative_item_carbon
        )

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

    # -----------------------------------------------------
    # 6. 추천안 선택
    # -----------------------------------------------------

    recommended = next(
        (
            alternative
            for alternative in alternatives
            if alternative.constraintsSatisfied
        ),
        None,
    )

    if recommended is not None:
        recommendation_reason = (
            "예산 및 사용자 조건을 만족하는 대안 중 "
            "탄소 감축 효과가 큰 대안을 선택했습니다."
        )

        recommended_alternative_id = (
            recommended.id
        )

    else:
        recommendation_reason = (
            "현재 조건을 모두 만족하는 대안을 "
            "찾지 못했습니다."
        )

        recommended_alternative_id = None

    # -----------------------------------------------------
    # 7. 최종 응답
    # -----------------------------------------------------

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
    )