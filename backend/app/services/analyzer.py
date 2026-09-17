from collections import defaultdict
from typing import Any


def aggregate_by_category(
    calculated_items: list[dict[str, Any]],
) -> list[dict[str, Any]]:
    """
    계산된 항목들을 category별로 묶어
    비용과 탄소배출량을 합산한다.

    탄소 데이터가 없는 경우 carbonKgCo2e는 None으로 유지한다.
    """

    category_totals: dict[str, dict[str, Any]] = defaultdict(
        lambda: {
            "costKrw": 0.0,
            "carbonKgCo2e": 0.0,
            "hasCarbonData": False,
        }
    )

    for item in calculated_items:
        category = str(item["category"])

        category_totals[category]["costKrw"] += float(
            item["costKrw"]
        )

        carbon = item.get("carbonKgCo2e")

        if carbon is not None:
            category_totals[category]["carbonKgCo2e"] += float(
                carbon
            )
            category_totals[category]["hasCarbonData"] = True

    result: list[dict[str, Any]] = []

    for category, values in category_totals.items():
        result.append(
            {
                "category": category,
                "costKrw": values["costKrw"],
                "carbonKgCo2e": (
                    values["carbonKgCo2e"]
                    if values["hasCarbonData"]
                    else None
                ),
            }
        )

    return result


def calculate_category_percentages(
    category_breakdown: list[dict[str, Any]],
) -> list[dict[str, Any]]:
    """
    탄소 데이터가 있는 category에 대해서만
    전체 배출량 대비 비율을 계산한다.
    """

    carbon_values = [
        float(item["carbonKgCo2e"])
        for item in category_breakdown
        if item.get("carbonKgCo2e") is not None
    ]

    total_carbon = sum(carbon_values)

    result: list[dict[str, Any]] = []

    for item in category_breakdown:
        carbon = item.get("carbonKgCo2e")

        if carbon is None or total_carbon == 0:
            percentage = None
        else:
            percentage = (
                float(carbon)
                / total_carbon
                * 100
            )

        result.append(
            {
                **item,
                "percentage": percentage,
            }
        )

    return result


def find_hotspots(
    category_breakdown: list[dict[str, Any]],
    limit: int = 3,
) -> list[dict[str, Any]]:
    """
    탄소 데이터가 존재하는 category만 대상으로
    배출량이 높은 순서대로 hotspot을 찾는다.
    """

    if limit <= 0:
        raise ValueError(
            "limit은 1 이상이어야 합니다."
        )

    breakdown = calculate_category_percentages(
        category_breakdown
    )

    available = [
        item
        for item in breakdown
        if item.get("carbonKgCo2e") is not None
    ]

    available.sort(
        key=lambda item: float(item["carbonKgCo2e"]),
        reverse=True,
    )

    return available[:limit]


def analyze_plan(
    calculated_items: list[dict[str, Any]],
    hotspot_limit: int = 3,
) -> dict[str, Any]:
    """
    전체 비용 및 탄소 분석 결과를 생성한다.

    탄소계수가 아직 연결되지 않았다면
    totalCarbonKgCo2e는 None이다.
    """

    total_cost = sum(
        float(item["costKrw"])
        for item in calculated_items
    )

    carbon_values = [
        float(item["carbonKgCo2e"])
        for item in calculated_items
        if item.get("carbonKgCo2e") is not None
    ]

    total_carbon = (
        sum(carbon_values)
        if carbon_values
        else None
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