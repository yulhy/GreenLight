from collections import defaultdict
from typing import Any


def aggregate_by_category(
    calculated_items: list[dict[str, Any]],
) -> list[dict[str, Any]]:
    """
    계산된 항목들을 카테고리별로 묶어서
    탄소배출량과 비용을 합산한다.
    """

    category_totals = defaultdict(
        lambda: {
            "carbonKgCo2e": 0.0,
            "costKrw": 0.0,
        }
    )

    for item in calculated_items:
        category = item["category"]

        category_totals[category]["carbonKgCo2e"] += float(
            item["carbonKgCo2e"]
        )

        category_totals[category]["costKrw"] += float(
            item["costKrw"]
        )

    return [
        {
            "category": category,
            "carbonKgCo2e": values["carbonKgCo2e"],
            "costKrw": values["costKrw"],
        }
        for category, values in category_totals.items()
    ]


def calculate_category_percentages(
    category_breakdown: list[dict[str, Any]],
) -> list[dict[str, Any]]:
    """
    전체 탄소배출량에서 각 카테고리가
    차지하는 비율을 계산한다.
    """

    total_carbon = sum(
        float(category["carbonKgCo2e"])
        for category in category_breakdown
    )

    result = []

    for category in category_breakdown:
        carbon = float(
            category["carbonKgCo2e"]
        )

        if total_carbon == 0:
            percentage = 0.0
        else:
            percentage = (
                carbon
                / total_carbon
                * 100
            )

        result.append(
            {
                **category,
                "percentage": percentage,
            }
        )

    return result


def find_hotspots(
    category_breakdown: list[dict[str, Any]],
    limit: int = 3,
) -> list[dict[str, Any]]:
    """
    탄소배출량이 높은 카테고리를 hotspot으로 반환한다.

    기본적으로 상위 3개 카테고리를 반환한다.
    """

    if limit <= 0:
        raise ValueError(
            "limit은 1 이상이어야 합니다."
        )

    categories_with_percentage = (
        calculate_category_percentages(
            category_breakdown
        )
    )

    sorted_categories = sorted(
        categories_with_percentage,
        key=lambda item: item["carbonKgCo2e"],
        reverse=True,
    )

    return sorted_categories[:limit]


def analyze_plan(
    calculated_items: list[dict[str, Any]],
    hotspot_limit: int = 3,
) -> dict[str, Any]:
    """
    계산된 행사 계획 항목을 기반으로
    전체 분석 결과를 생성한다.
    """

    total_carbon = sum(
        float(item["carbonKgCo2e"])
        for item in calculated_items
    )

    total_cost = sum(
        float(item["costKrw"])
        for item in calculated_items
    )

    category_breakdown = aggregate_by_category(
        calculated_items
    )

    hotspots = find_hotspots(
        category_breakdown,
        limit=hotspot_limit,
    )

    return {
        "totalCarbonKgCo2e": total_carbon,
        "totalCostKrw": total_cost,
        "categoryBreakdown": category_breakdown,
        "hotspots": hotspots,
    }
