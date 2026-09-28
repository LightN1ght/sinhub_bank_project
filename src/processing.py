from typing import Any


def filter_by_state(dict_list: list[dict[str, Any]], state: str = "EXECUTED") -> list[dict[str, Any]]:
    result = []
    for item in dict_list:
        if item["state"] == state:
            result.append(item)

    return result
