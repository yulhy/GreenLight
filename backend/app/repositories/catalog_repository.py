import os
from pathlib import Path

import pandas as pd


DEFAULT_CATALOG_PATH = (
    Path(__file__).resolve().parent.parent
    / "data"
    / "catalog.csv"
)


def get_catalog_path() -> Path:
    """
    환경변수 CATALOG_CSV_PATH가 있으면 해당 경로를 사용하고,
    없으면 backend/app/data/catalog.csv를 사용한다.
    """

    path = os.getenv("CATALOG_CSV_PATH")

    if path:
        return Path(path)

    return DEFAULT_CATALOG_PATH


def load_catalog() -> pd.DataFrame:
    """
    catalog.csv 전체 데이터를 불러온다.
    """

    catalog_path = get_catalog_path()

    if not catalog_path.exists():
        raise FileNotFoundError(
            f"Catalog CSV 파일을 찾을 수 없습니다: {catalog_path}"
        )

    catalog = pd.read_csv(catalog_path)

    required_columns = {
        "category",
        "item_id",
        "item_name",
        "carbon_factor",
        "unit",
        "reference_cost_krw",
    }

    missing_columns = (
        required_columns - set(catalog.columns)
    )

    if missing_columns:
        raise ValueError(
            "catalog.csv에 필요한 컬럼이 없습니다: "
            + ", ".join(sorted(missing_columns))
        )

    return catalog


def get_categories() -> list[str]:
    """
    카탈로그에 존재하는 카테고리 목록을 반환한다.
    """

    catalog = load_catalog()

    return sorted(
        catalog["category"]
        .dropna()
        .astype(str)
        .unique()
        .tolist()
    )


def get_items_by_category(
    category: str,
) -> pd.DataFrame:
    """
    특정 카테고리의 모든 항목을 반환한다.
    """

    catalog = load_catalog()

    return catalog[
        catalog["category"] == category
    ].copy()


def get_item_by_id(
    item_id: str,
) -> dict | None:
    """
    item_id로 카탈로그 항목을 조회한다.
    """

    catalog = load_catalog()

    matched = catalog[
        catalog["item_id"] == item_id
    ]

    if matched.empty:
        return None

    return matched.iloc[0].to_dict()


def get_item(
    category: str,
    item_id: str,
) -> dict | None:
    """
    category + item_id 조합으로 항목을 조회한다.
    """

    catalog = load_catalog()

    matched = catalog[
        (catalog["category"] == category)
        & (catalog["item_id"] == item_id)
    ]

    if matched.empty:
        return None

    return matched.iloc[0].to_dict()


def get_alternatives(
    category: str,
    current_item_id: str,
) -> pd.DataFrame:
    """
    현재 항목을 제외하고,
    같은 카테고리의 대안 후보를 반환한다.
    """

    catalog = load_catalog()

    alternatives = catalog[
        (catalog["category"] == category)
        & (catalog["item_id"] != current_item_id)
    ]

    return alternatives.copy()