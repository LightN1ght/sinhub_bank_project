import logging

import pandas as pd

logger = logging.getLogger(__name__)


def simple_search(transactions: pd.DataFrame, query: str) -> str:
    """Возвращает JSON с операциями, найденными в описании или категории"""
    search_text = query.strip().casefold()

    if not search_text:
        return "[]"

    def contains_query(value: object) -> bool:
        return search_text in str(value).casefold()

    description_matches = transactions["Описание"].fillna("").map(contains_query)
    category_matches = transactions["Категория"].fillna("").map(contains_query)
    matches = transactions.loc[description_matches | category_matches]

    logger.info("Найдено операций: %d", len(matches))
    return matches.to_json(orient="records", force_ascii=False, date_format="iso")