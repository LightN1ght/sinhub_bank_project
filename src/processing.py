from typing import Any, Literal
from datetime import datetime


def filter_by_state(dict_list: list[dict[str, Any]], state: str = "EXECUTED") -> list[dict[str, Any]]:
    result = []
    for item in dict_list:
        if item["state"] == state:
            result.append(item)

    return result

def sort_by_date(dict_list: list[dict[str, Any]], order: Literal["asc", "desc"] = "desc") -> list[dict[str, Any]]:
    return sorted(dict_list, key = lambda item: datetime.fromisoformat(item["date"]), reverse=order == "desc")
