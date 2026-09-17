from typing import Any


def check_budget(
    alternative_cost: float,
    budget_krw: float | None,
) -> tuple[bool, str | None]:
    """
    대안의 총 비용이 사용자의 전체 예산을 초과하는지 확인한다.
    """

    if budget_krw is None:
        return True, None

    if alternative_cost <= budget_krw:
        return True, None

    return (
        False,
        (
            f"대안 비용 {alternative_cost:.0f}원이 "
            f"예산 {budget_krw:.0f}원을 초과합니다."
        ),
    )


def check_additional_cost(
    baseline_cost: float,
    alternative_cost: float,
    max_additional_cost_krw: float | None,
) -> tuple[bool, str | None]:
    """
    기존 계획 대비 추가 비용이
    사용자가 허용한 범위를 초과하는지 확인한다.
    """

    if max_additional_cost_krw is None:
        return True, None

    additional_cost = (
        alternative_cost
        - baseline_cost
    )

    if additional_cost <= max_additional_cost_krw:
        return True, None

    return (
        False,
        (
            f"추가 비용 {additional_cost:.0f}원이 "
            f"허용 범위 {max_additional_cost_krw:.0f}원을 초과합니다."
        ),
    )


def check_avoided_items(
    alternative_items: list[str],
    avoid_items: list[str] | None,
) -> tuple[bool, str | None]:
    """
    사용자가 피하고 싶다고 지정한 항목이
    대안에 포함되어 있는지 확인한다.
    """

    if not avoid_items:
        return True, None

    normalized_avoid_items = {
        item.strip().lower()
        for item in avoid_items
    }

    for item in alternative_items:
        if item.strip().lower() in normalized_avoid_items:
            return (
                False,
                f"사용자가 제외한 항목 '{item}'이 포함되어 있습니다.",
            )

    return True, None


def evaluate_feasibility(
    *,
    baseline_cost: float,
    alternative_cost: float,
    budget_krw: float | None = None,
    max_additional_cost_krw: float | None = None,
    alternative_items: list[str] | None = None,
    avoid_items: list[str] | None = None,
) -> dict[str, Any]:
    """
    대안이 사용자의 조건을 만족하는지 종합 검증한다.

    반환값:
    {
        "feasible": bool,
        "reasons": list[str],
        "additionalCostKrw": float
    }
    """

    reasons: list[str] = []

    budget_ok, budget_reason = check_budget(
        alternative_cost=alternative_cost,
        budget_krw=budget_krw,
    )

    if not budget_ok and budget_reason:
        reasons.append(budget_reason)

    additional_cost_ok, additional_cost_reason = (
        check_additional_cost(
            baseline_cost=baseline_cost,
            alternative_cost=alternative_cost,
            max_additional_cost_krw=max_additional_cost_krw,
        )
    )

    if (
        not additional_cost_ok
        and additional_cost_reason
    ):
        reasons.append(additional_cost_reason)

    avoided_items_ok, avoided_items_reason = (
        check_avoided_items(
            alternative_items=alternative_items or [],
            avoid_items=avoid_items,
        )
    )

    if (
        not avoided_items_ok
        and avoided_items_reason
    ):
        reasons.append(avoided_items_reason)

    additional_cost = (
        alternative_cost
        - baseline_cost
    )

    return {
        "feasible": len(reasons) == 0,
        "reasons": reasons,
        "additionalCostKrw": additional_cost,
    }
