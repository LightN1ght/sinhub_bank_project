import json

import pandas as pd

from src.services import simple_search


def test_simple_search_finds_description_and_category() -> None:
    transactions = pd.DataFrame(
        [
            {"Описание": "Кофе в кафе", "Категория": "Рестораны"},
            {"Описание": "Оплата", "Категория": "Кофейни"},
            {"Описание": "КОФЕ", "Категория": "кофе"},
            {"Описание": "Такси", "Категория": None},
        ]
    )

    result = json.loads(simple_search(transactions, "кофе"))

    assert [item["Описание"] for item in result] == [
        "Кофе в кафе",
        "Оплата",
        "КОФЕ",
    ]


def test_simple_search_returns_empty_list_when_nothing_found() -> None:
    transactions = pd.DataFrame([{"Описание": "Такси", "Категория": None}])

    assert json.loads(simple_search(transactions, "аптека")) == []


def test_simple_search_returns_empty_list_for_blank_query() -> None:
    transactions = pd.DataFrame([{"Описание": "Такси", "Категория": "Транспорт"}])

    assert json.loads(simple_search(transactions, "   ")) == []
