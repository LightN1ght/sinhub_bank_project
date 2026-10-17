import re
from datetime import datetime
from typing import Any
from collections import Counter


def filter_by_state(dict_list: list[dict[str, Any]], state: str = "EXECUTED") -> list[dict[str, Any]]:
    """Функция, которая фильтрует список только с элементами с указанным состоянием, по умолчанию EXECUTED"""
    result = []
    for item in dict_list:
        if item["state"] == state:
            result.append(item)

    return result


def sort_by_date(dict_list: list[dict[str, Any]], is_reversed: bool = True) -> list[dict[str, Any]]:
    """Функция, которая сортирует список по дате, по умолчанию по убыванию"""
    return sorted(dict_list, key=lambda item: datetime.fromisoformat(item["date"]), reverse=is_reversed)

def process_bank_search(
        data: list[dict[str, Any]],
        search: str,
) -> list[dict[str, Any]]:
    """Поиск строки в описаниях транзакций"""
    result = []

    for transaction in data:
        description = transaction["description"]

        if re.search(re.escape(search), description, flags=re.IGNORECASE):
            result.append(transaction)

    return result

def process_bank_operations(
    data: list[dict[str, Any]],
    categories: list[str],
) -> dict[str, int]:
    """Подсчитывает количество операций для каждой категории"""
    descriptions = []

    for transaction in data:
        descriptions.append(transaction["description"])

    counts = Counter(descriptions)
    result = {}

    for category in categories:
        result[category] = counts[category]

    return result
