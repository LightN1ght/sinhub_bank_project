from datetime import datetime
from typing import Any, Literal


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
