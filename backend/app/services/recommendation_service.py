from typing import Any

from app.repositories.catalog_repository import get_alternatives
from app.rules.feasibility import evaluate_feasibility
from app.services.calculator import (
    calculate_cost_difference,
    calculate_item,
    calculate_reduction,
)


def build_recommendations(
    *,
    category: str,
    current_item_id: str,
    current_item_name: str,
    quantity: float,
    baseline_carbon: float,
    baseline_cost: float,
    budget_krw: float | None = None,
    max_additional_cost_krw: float | None = None,
    avoid_items: list[str] | None = None,
) -> list[dict[str, Any]]:
    """
    특정 카테고리의 현재 선택 항목을 기준으로
    친환경 대안 후보를 생성한다.
    """

    alternatives = get_alternatives(
        category=category,
        current_item_id=current_item_id,
    )

    recommendations: list[dict[str, Any]] = []

    for _, row in alternatives.iterrows():
        alternative_data = row.to_dict()

        calculated = calculate_item(
            item=alternative_data,
            quantity=quantity,
        )

        alternative_carbon = float(
            calculated["carbonKgCo2e"]
        )

        alternative_cost = float(
            calculated["costKrw"]
        )

        reduction = calculate_reduction(
            baseline_carbon=baseline_carbon,
            alternative_carbon=alternative_carbon,
        )

        # 탄소 감축 효과가 없는 항목은 제외
        if reduction["carbonReductionKgCo2e"] <= 0:
            continue

        additional_cost = calculate_cost_difference(
            baseline_cost=baseline_cost,
            alternative_cost=alternative_cost,
        )

        feasibility = evaluate_feasibility(
            baseline_cost=baseline_cost,
            alternative_cost=alternative_cost,
            budget_krw=budget_krw,
            max_additional_cost_krw=max_additional_cost_krw,
            alternative_items=[
                str(calculated["itemName"])
            ],
            avoid_items=avoid_items,
        )

        recommendations.append(
            {
                "category": category,

                "originalItemId": current_item_id,
                "originalItem": current_item_name,

                "alternativeItemId": calculated["itemId"],
                "alternativeItem": calculated["itemName"],

                "quantity": quantity,

                "baselineCarbonKgCo2e": baseline_carbon,
                "alternativeCarbonKgCo2e": alternative_carbon,

                "carbonReductionKgCo2e": reduction[
                    "carbonReductionKgCo2e"
                ],
                "carbonReductionPercent": reduction[
                    "carbonReductionPercent"
                ],

                "baselineCostKrw": baseline_cost,
                "alternativeCostKrw": alternative_cost,
                "additionalCostKrw": additional_cost,

                "feasible": feasibility["feasible"],
                "feasibilityReasons": feasibility["reasons"],
            }
        )

    return recommendations


def sort_recommendations(
    recommendations: list[dict[str, Any]],
) -> list[dict[str, Any]]:
    """
    추천 후보를 정렬한다.

    우선순위:
    1. 실행 가능한 대안
    2. 탄소 감축량이 큰 대안
    """

    return sorted(
        recommendations,
        key=lambda recommendation: (
            not recommendation["feasible"],
            -float(
                recommendation[
                    "carbonReductionKgCo2e"
                ]
            ),
        ),
    )


def recommend_for_item(
    *,
    category: str,
    current_item_id: str,
    current_item_name: str,
    quantity: float,
    baseline_carbon: float,
    baseline_cost: float,
    budget_krw: float | None = None,
    max_additional_cost_krw: float | None = None,
    avoid_items: list[str] | None = None,
    limit: int = 3,
) -> list[dict[str, Any]]:
    """
    현재 선택 항목 하나에 대한 최종 추천 후보를 반환한다.
    """

    if limit <= 0:
        raise ValueError(
            "limit은 1 이상이어야 합니다."
        )

    recommendations = build_recommendations(
        category=category,
        current_item_id=current_item_id,
        current_item_name=current_item_name,
        quantity=quantity,
        baseline_carbon=baseline_carbon,
        baseline_cost=baseline_cost,
        budget_krw=budget_krw,
        max_additional_cost_krw=max_additional_cost_krw,
        avoid_items=avoid_items,
    )

    return sort_recommendations(
        recommendations
    )[:limit]


def recommend_for_hotspots(
    *,
    calculated_items: list[dict[str, Any]],
    hotspots: list[dict[str, Any]],
    budget_krw: float | None = None,
    max_additional_cost_krw: float | None = None,
    avoid_items: list[str] | None = None,
    limit_per_item: int = 3,
) -> list[dict[str, Any]]:
    """
    Hotspot으로 식별된 카테고리에 속한 현재 항목들에 대해
    대안을 생성한다.
    """

    hotspot_categories = {
        hotspot["category"]
        for hotspot in hotspots
    }

    recommendations: list[dict[str, Any]] = []

    for item in calculated_items:
        category = item["category"]

        if category not in hotspot_categories:
            continue

        item_recommendations = recommend_for_item(
            category=category,
            current_item_id=item["itemId"],
            current_item_name=item["itemName"],
            quantity=float(item["quantity"]),
            baseline_carbon=float(
                item["carbonKgCo2e"]
            ),
            baseline_cost=float(
                item["costKrw"]
            ),
            budget_krw=budget_krw,
            max_additional_cost_krw=max_additional_cost_krw,
            avoid_items=avoid_items,
            limit=limit_per_item,
        )

        recommendations.extend(
            item_recommendations
        )

    return sort_recommendations(
        recommendations
    )