import os
from pathlib import Path

import pandas as pd


# =========================================================
# Paths
# =========================================================

DEFAULT_COST_DATA_PATH = (
    Path(__file__).resolve().parent.parent
    / "data"
    / "event_costs_english.xlsx"
)


def get_cost_data_path() -> Path:
    """
    COST_DATA_PATH 환경변수가 있으면 해당 경로를 사용하고,
    없으면 backend/app/data/event_costs_english.xlsx를 사용한다.
    """

    path = os.getenv("COST_DATA_PATH")

    if path:
        return Path(path)

    return DEFAULT_COST_DATA_PATH


# =========================================================
# Load
# =========================================================

def load_cost_catalog() -> pd.DataFrame:
    """
    event_costs_english.xlsx의 비용 데이터를 불러온다.

    원본 엑셀은 수정하지 않고 읽기 전용으로 사용한다.
    """

    path = get_cost_data_path()

    if not path.exists():
        raise FileNotFoundError(
            f"비용 데이터 파일을 찾을 수 없습니다: {path}"
        )

    catalog = pd.read_excel(
        path,
        sheet_name="event_costs.csv",
    )

    required_columns = {
        "item_id",
        "category",
        "item_name",
        "unit",
        "unit_price_krw",
        "pricing_method",
    }

    missing_columns = (
        required_columns
        - set(catalog.columns)
    )

    if missing_columns:
        raise ValueError(
            "비용 데이터에 필요한 컬럼이 없습니다: "
            + ", ".join(
                sorted(missing_columns)
            )
        )

    return catalog


# =========================================================
# Category
# =========================================================

def get_categories() -> list[str]:
    """
    비용 데이터에 등록된 category 목록을 반환한다.
    """

    catalog = load_cost_catalog()

    categories = (
        catalog["category"]
        .dropna()
        .astype(str)
        .unique()
        .tolist()
    )

    return sorted(categories)


def get_items_by_category(
    category: str,
) -> pd.DataFrame:
    """
    특정 category의 모든 항목을 반환한다.
    """

    catalog = load_cost_catalog()

    return catalog[
        catalog["category"] == category
    ].copy()


# =========================================================
# Item
# =========================================================

def get_item_by_id(
    item_id: str,
) -> dict | None:
    """
    item_id만으로 항목을 조회한다.
    """

    catalog = load_cost_catalog()

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

    catalog = load_cost_catalog()

    matched = catalog[
        (catalog["category"] == category)
        & (catalog["item_id"] == item_id)
    ]

    if matched.empty:
        return None

    return matched.iloc[0].to_dict()


# =========================================================
# Alternatives
# =========================================================

def get_alternatives(
    category: str,
    current_item_id: str,
) -> pd.DataFrame:
    """
    같은 category에서 현재 항목을 제외한
    대안 후보들을 반환한다.
    """

    catalog = load_cost_catalog()

    alternatives = catalog[
        (catalog["category"] == category)
        & (catalog["item_id"] != current_item_id)
    ]

    return alternatives.copy()


# =========================================================
# Search by name
# =========================================================

def find_items_by_name(
    category: str,
    query: str,
) -> pd.DataFrame:
    """
    사용자 자연어와 카탈로그 item_name을
    연결할 때 사용할 이름 검색 함수.

    대소문자를 구분하지 않고 부분 일치로 검색한다.
    """

    catalog = load_cost_catalog()

    category_items = catalog[
        catalog["category"] == category
    ]

    if not query.strip():
        return category_items.iloc[0:0].copy()

    normalized_query = (
        query
        .strip()
        .lower()
    )

    matched = category_items[
        category_items["item_name"]
        .astype(str)
        .str.lower()
        .str.contains(
            normalized_query,
            regex=False,
            na=False,
        )
    ]

    return matched.copy()