from typing import Any


def calculate_carbon(
    carbon_factor: float,
    quantity: float,
) -> float:
    """
    탄소배출량을 계산한다.

    탄소배출량 = carbon_factor × quantity
    """

    if carbon_factor < 0:
        raise ValueError(
            "carbon_factor는 0 이상이어야 합니다."
        )

    if quantity < 0:
        raise ValueError(
            "quantity는 0 이상이어야 합니다."
        )

    return carbon_factor * quantity


def calculate_cost(
    reference_cost_krw: float,
    quantity: float,
) -> float:
    """
    비용을 계산한다.

    비용 = 기준 비용 × quantity
    """

    if reference_cost_krw < 0:
        raise ValueError(
            "reference_cost_krw는 0 이상이어야 합니다."
        )

    if quantity < 0:
        raise ValueError(
            "quantity는 0 이상이어야 합니다."
        )

    return reference_cost_krw * quantity


def calculate_item(
    item: dict[str, Any],
    quantity: float,
) -> dict[str, Any]:
    """
    catalog 항목 하나의 탄소배출량과 비용을 계산한다.

    필요한 필드:
    - category
    - item_id
    - item_name
    - carbon_factor
    - reference_cost_krw
    - unit
    """

    required_fields = {
        "category",
        "item_id",
        "item_name",
        "carbon_factor",
        "reference_cost_krw",
        "unit",
    }

    missing_fields = (
        required_fields - set(item.keys())
    )

    if missing_fields:
        raise ValueError(
            "계산에 필요한 catalog 필드가 없습니다: "
            + ", ".join(sorted(missing_fields))
        )

    carbon_factor = float(
        item["carbon_factor"]
    )

    reference_cost_krw = float(
        item["reference_cost_krw"]
    )

    carbon = calculate_carbon(
        carbon_factor=carbon_factor,
        quantity=quantity,
    )

    cost = calculate_cost(
        reference_cost_krw=reference_cost_krw,
        quantity=quantity,
    )

    return {
        "category": item["category"],
        "itemId": item["item_id"],
        "itemName": item["item_name"],
        "quantity": quantity,
        "unit": item["unit"],
        "carbonFactor": carbon_factor,
        "referenceCostKrw": reference_cost_krw,
        "carbonKgCo2e": carbon,
        "costKrw": cost,
    }


def calculate_total(
    calculated_items: list[dict[str, Any]],
) -> dict[str, float]:
    """
    여러 항목의 총 탄소배출량과 총 비용을 계산한다.
    """

    total_carbon = sum(
        float(item["carbonKgCo2e"])
        for item in calculated_items
    )

    total_cost = sum(
        float(item["costKrw"])
        for item in calculated_items
    )

    return {
        "totalCarbonKgCo2e": total_carbon,
        "totalCostKrw": total_cost,
    }


def calculate_reduction(
    baseline_carbon: float,
    alternative_carbon: float,
) -> dict[str, float]:
    """
    기존 계획 대비 탄소 감축량과 감축률을 계산한다.
    """

    if baseline_carbon < 0:
        raise ValueError(
            "baseline_carbon은 0 이상이어야 합니다."
        )

    if alternative_carbon < 0:
        raise ValueError(
            "alternative_carbon은 0 이상이어야 합니다."
        )

    reduction = (
        baseline_carbon
        - alternative_carbon
    )

    if baseline_carbon == 0:
        reduction_percent = 0.0
    else:
        reduction_percent = (
            reduction
            / baseline_carbon
            * 100
        )

    return {
        "carbonReductionKgCo2e": reduction,
        "carbonReductionPercent": reduction_percent,
    }


def calculate_cost_difference(
    baseline_cost: float,
    alternative_cost: float,
) -> float:
    """
    기존 계획 대비 대안의 비용 차이를 계산한다.

    양수:
        대안이 더 비쌈

    음수:
        대안이 더 저렴함
    """

    return alternative_cost - baseline_cost