from datetime import (
    date,
    datetime,
)
from typing import Any

import pandas as pd
from fastapi import (
    APIRouter,
    HTTPException,
)

from app.repositories.catalog_repository import (
    get_categories,
    get_item,
    get_items_by_category,
)


router = APIRouter(
    tags=["Catalog"],
)


def _json_safe(
    value: Any,
) -> Any:
    if value is None:
        return None

    try:
        if pd.isna(value):
            return None
    except (
        TypeError,
        ValueError,
    ):
        pass


    if isinstance(
        value,
        (datetime, date),
    ):
        return value.isoformat()


    if hasattr(value, "item"):
        try:
            return value.item()
        except (
            ValueError,
            AttributeError,
        ):
            pass


    return value


def _record_to_json(
    record: dict,
) -> dict:
    return {
        key: _json_safe(value)
        for key, value
        in record.items()
    }


@router.get(
    "/catalog/categories",
)
async def list_categories():
    return {
        "categories":
            get_categories(),
    }


@router.get(
    "/catalog/items",
)
async def list_items(
    category: str,
):
    items = get_items_by_category(
            category
        )

    records = [
        _record_to_json(record)
        for record
        in items.to_dict(
            orient="records",
        )
    ]

    return {
        "items": records,
    }


@router.get(
    "/catalog/items/{item_id}",
)
async def get_catalog_item(
    item_id: str,
    category: str,
):
    item = get_item(
        category=category,
        item_id=item_id,
    )


    if item is None:
        raise HTTPException(
            status_code=404,
            detail=(
                "카탈로그 항목을 찾을 수 없습니다: "
                f"{category}/{item_id}"
            ),
        )


    return _record_to_json(item)