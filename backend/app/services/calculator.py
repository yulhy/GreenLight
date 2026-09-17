from typing import Any


def calculate_activity_quantity(
    *,
    unit: str,
    participant_count: int,
    round_trip_distance_km: float = 0,
    duration_days: int = 1,
    vehicle_count: int | None = None,
    meal_count: int | None = None,
    item_count: int | None = None,
    page_count: int | None = None,
    can_count: int | None = None,
    rental_item_count: int | None = None,
    rental_nights: int | None = None,
) -> float:
    """
    원본 비용 데이터의 unit 기준으로 실제 계산 quantity를 만든다.

    지원 unit:
    - person_night
    - person_meal
    - person_item
    - page
    - item
    - vehicle_km
    - person_km
    - can
    - item_night
    """

    if participant_count <= 0:
        raise ValueError(
            "participant_count는 1 이상이어야 합니다."
        )

    if round_trip_distance_km < 0:
        raise ValueError(
            "round_trip_distance_km는 0 이상이어야 합니다."
        )

    if duration_days <= 0:
        raise ValueError(
            "duration_days는 1 이상이어야 합니다."
        )

    # -----------------------------------------
    # 숙박
    # -----------------------------------------

    if unit == "person_night":
        nights = max(
            duration_days - 1,
            0,
        )

        return (
            participant_count
            * nights
        )

    # -----------------------------------------
    # 식사 / 취사
    # -----------------------------------------

    if unit == "person_meal":
        if meal_count is None:
            raise ValueError(
                "person_meal 계산에는 "
                "meal_count가 필요합니다."
            )

        if meal_count < 0:
            raise ValueError(
                "meal_count는 0 이상이어야 합니다."
            )

        return (
            participant_count
            * meal_count
        )

    # -----------------------------------------
    # 간식 / 음료 등
    # -----------------------------------------

    if unit == "person_item":
        if item_count is None:
            raise ValueError(
                "person_item 계산에는 "
                "item_count가 필요합니다."
            )

        if item_count < 0:
            raise ValueError(
                "item_count는 0 이상이어야 합니다."
            )

        return (
            participant_count
            * item_count
        )

    # -----------------------------------------
    # 교통
    # -----------------------------------------

    if unit == "vehicle_km":
        if vehicle_count is None:
            raise ValueError(
                "vehicle_km 계산에는 "
                "vehicle_count가 필요합니다."
            )

        if vehicle_count <= 0:
            raise ValueError(
                "vehicle_count는 1 이상이어야 합니다."
            )

        return (
            vehicle_count
            * round_trip_distance_km
        )

    if unit == "person_km":
        return (
            participant_count
            * round_trip_distance_km
        )

    # -----------------------------------------
    # 인쇄
    # -----------------------------------------

    if unit == "page":
        if page_count is None:
            raise ValueError(
                "page 계산에는 "
                "page_count가 필요합니다."
            )

        if page_count < 0:
            raise ValueError(
                "page_count는 0 이상이어야 합니다."
            )

        return float(
            page_count
        )

    # -----------------------------------------
    # 일반 물품
    # -----------------------------------------

    if unit == "item":
        if item_count is None:
            raise ValueError(
                "item 계산에는 "
                "item_count가 필요합니다."
            )

        if item_count < 0:
            raise ValueError(
                "item_count는 0 이상이어야 합니다."
            )

        return float(
            item_count
        )

    # -----------------------------------------
    # 가스통 등
    # -----------------------------------------

    if unit == "can":
        if can_count is None:
            raise ValueError(
                "can 계산에는 "
                "can_count가 필요합니다."
            )

        if can_count < 0:
            raise ValueError(
                "can_count는 0 이상이어야 합니다."
            )

        return float(
            can_count
        )

    # -----------------------------------------
    # 대여 물품 × 숙박일
    # -----------------------------------------

    if unit == "item_night":
        if rental_item_count is None:
            raise ValueError(
                "item_night 계산에는 "
                "rental_item_count가 필요합니다."
            )

        if rental_item_count < 0:
            raise ValueError(
                "rental_item_count는 0 이상이어야 합니다."
            )

        nights = (
            rental_nights
            if rental_nights is not None
            else max(
                duration_days - 1,
                0,
            )
        )

        if nights < 0:
            raise ValueError(
                "rental_nights는 0 이상이어야 합니다."
            )

        return (
            rental_item_count
            * nights
        )

    raise ValueError(
        f"지원하지 않는 unit입니다: {unit}"
    )


def calculate_cost(
    unit_price_krw: float,
    quantity: float,
) -> float:
    """
    비용 = 단위 가격 × 활동량
    """

    if unit_price_krw < 0:
        raise ValueError(
            "unit_price_krw는 0 이상이어야 합니다."
        )

    if quantity < 0:
        raise ValueError(
            "quantity는 0 이상이어야 합니다."
        )

    return (
        unit_price_krw
        * quantity
    )


def calculate_carbon(
    carbon_factor: float,
    quantity: float,
) -> float:
    """
    탄소배출량 = 탄소배출계수 × 활동량

    탄소계수 데이터는 추후 비용 데이터와
    별도로 연결한다.
    """

    if carbon_factor < 0:
        raise ValueError(
            "carbon_factor는 0 이상이어야 합니다."
        )

    if quantity < 0:
        raise ValueError(
            "quantity는 0 이상이어야 합니다."
        )

    return (
        carbon_factor
        * quantity
    )


def calculate_item(
    item: dict[str, Any],
    quantity: float,
    *,
    carbon_factor: float | None = None,
) -> dict[str, Any]:
    """
    비용 데이터의 단일 항목을 계산한다.

    원본 event_costs 데이터 기준 필수 필드:
    - item_id
    - category
    - item_name
    - unit
    - unit_price_krw

    carbon_factor가 제공되면 탄소배출량도 계산한다.
    아직 탄소 데이터가 없으면 None을 반환한다.
    """

    required_fields = {
        "item_id",
        "category",
        "item_name",
        "unit",
        "unit_price_krw",
    }

    missing_fields = (
        required_fields
        - set(item.keys())
    )

    if missing_fields:
        raise ValueError(
            "계산에 필요한 비용 데이터 필드가 없습니다: "
            + ", ".join(
                sorted(missing_fields)
            )
        )

    unit_price_krw = float(
        item["unit_price_krw"]
    )

    cost = calculate_cost(
        unit_price_krw=unit_price_krw,
        quantity=quantity,
    )

    carbon = None

    if carbon_factor is not None:
        carbon = calculate_carbon(
            carbon_factor=carbon_factor,
            quantity=quantity,
        )

    return {
        "category": item["category"],
        "itemId": item["item_id"],
        "itemName": item["item_name"],
        "unit": item["unit"],
        "quantity": quantity,
        "unitPriceKrw": unit_price_krw,
        "costKrw": cost,
        "carbonFactor": carbon_factor,
        "carbonKgCo2e": carbon,
    }


def calculate_total_cost(
    calculated_items: list[dict[str, Any]],
) -> float:
    """
    여러 항목의 총 비용을 계산한다.
    """

    return sum(
        float(item["costKrw"])
        for item in calculated_items
    )


def calculate_total_carbon(
    calculated_items: list[dict[str, Any]],
) -> float:
    """
    탄소 값이 존재하는 항목들의
    총 탄소배출량을 계산한다.
    """

    return sum(
        float(item["carbonKgCo2e"])
        for item in calculated_items
        if item.get("carbonKgCo2e")
        is not None
    )


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
    기존 계획 대비 대안 비용 차이.

    양수 = 대안이 더 비쌈
    음수 = 대안이 더 저렴함
    """

    return (
        alternative_cost
        - baseline_cost
    )