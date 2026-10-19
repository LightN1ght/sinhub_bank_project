from datetime import datetime

import pandas as pd
import pytest

from src.views import get_greeting, select_month_transactions, get_cards_info, get_top_transactions


@pytest.mark.parametrize(
    ("time", "expected"),
    [
        ("05:59:59", "Доброй ночи"),
        ("06:00:00", "Доброе утро"),
        ("11:59:59", "Доброе утро"),
        ("12:00:00", "Добрый день"),
        ("17:59:59", "Добрый день"),
        ("18:00:00", "Добрый вечер"),
        ("22:59:59", "Добрый вечер"),
        ("23:00:00", "Доброй ночи"),
    ],
)
def test_get_greeting_at_boundaries(time: str, expected: str) -> None:
    current_time = datetime.strptime(time, "%H:%M:%S")

    assert get_greeting(current_time) == expected


def test_select_month_transactions_includes_both_boundaries() -> None:
    transactions = pd.DataFrame(
        {
            "Дата операции": pd.to_datetime(
                [
                    "2021-11-30 23:59:59",
                    "2021-12-01 00:00:00",
                    "2021-12-20 12:00:00",
                    "2021-12-20 12:00:01",
                ]
            ),
            "Описание": ["прошлый месяц", "начало", "до даты", "после даты"],
        }
    )

    result = select_month_transactions(transactions, "2021-12-20 12:00:00")

    assert result["Описание"].tolist() == ["начало", "до даты"]

def test_get_cards_info_counts_successful_expenses() -> None:
    transactions = pd.DataFrame(
        [
            {"Номер карты": "*1234", "Статус": "OK", "Сумма платежа": -150.0, "Валюта платежа": "RUB"},
            {"Номер карты": "*1234", "Статус": "OK", "Сумма платежа": -50.0, "Валюта платежа": "RUB"},
            {"Номер карты": "*1234", "Статус": "FAILED", "Сумма платежа": -1000.0, "Валюта платежа": "RUB"},
            {"Номер карты": "*1234", "Статус": "OK", "Сумма платежа": 20.0, "Валюта платежа": "RUB"},
            {"Номер карты": "*9876", "Статус": "OK", "Сумма платежа": -7.94, "Валюта платежа": "RUB"},
            {"Номер карты": None, "Статус": "OK", "Сумма платежа": -300.0, "Валюта платежа": "RUB"},
        ]
    )

    assert get_cards_info(transactions) == [
        {"last_digits": "1234", "total_spent": 200.0, "cashback": 2.0},
        {"last_digits": "9876", "total_spent": 7.94, "cashback": 0.08},
    ]

def test_get_top_transactions_sorts_amount_and_skips_failed() -> None:
    transactions = pd.DataFrame(
        {
            "Дата операции": pd.to_datetime(["2021-12-01"] * 6),
            "Статус": ["OK", "OK", "OK", "OK", "OK", "FAILED"],
            "Сумма платежа": [120, -50, 10, 300, -200, 999],
            "Категория": ["A", "B", "C", "D", None, "F"],
            "Описание": ["one", "two", "three", "four", "five", "failed"],
        }
    )

    result = get_top_transactions(transactions)

    assert [item["amount"] for item in result] == [300, 120, 10, -50, -200]
    assert all(item["date"] == "01.12.2021" for item in result)
    assert all(
        set(item) == {"date", "amount", "category", "description"}
        for item in result
    )
    assert result[-1]["category"] == ""