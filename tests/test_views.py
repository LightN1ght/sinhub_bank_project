import json
from datetime import datetime
from unittest.mock import patch

import pandas as pd
import pytest

from src.views import (
    build_home_page,
    get_cards_info,
    get_greeting,
    get_top_transactions,
    main_page,
    select_month_transactions,
)


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
            "Валюта платежа": ["RUB"] * 6,
        }
    )

    result = get_top_transactions(transactions)

    assert [item["amount"] for item in result] == [300, 120, 10, -50, -200]
    assert all(item["date"] == "01.12.2021" for item in result)
    assert all(set(item) == {"date", "amount", "category", "description"} for item in result)
    assert result[-1]["category"] == ""


def test_build_home_page_combines_month_data() -> None:
    transactions = pd.DataFrame(
        {
            "Дата операции": pd.to_datetime(
                [
                    "2021-11-30 23:59:59",
                    "2021-12-01 00:00:00",
                    "2021-12-03 10:00:00",
                    "2021-12-05 10:00:00",
                    "2021-12-10 10:00:00",
                    "2021-12-15 10:00:00",
                    "2021-12-20 12:00:00",
                    "2021-12-20 12:00:01",
                ]
            ),
            "Статус": ["OK", "OK", "OK", "OK", "OK", "FAILED", "OK", "OK"],
            "Номер карты": [
                None,
                "*1234",
                "*1234",
                None,
                "*1234",
                "*1234",
                "*9876",
                None,
            ],
            "Сумма платежа": [999, -100, -50, 200, -25, 1000, -10, 9999],
            "Валюта платежа": ["RUB"] * 8,
            "Категория": ["Тест"] * 8,
            "Описание": [f"Операция {i}" for i in range(8)],
        }
    )
    settings = {
        "user_currencies": ["USD", "EUR"],
        "user_stocks": ["AAPL", "MSFT"],
    }
    rates = [
        {"currency": "USD", "rate": 82.0},
        {"currency": "EUR", "rate": 92.0},
    ]
    prices = [
        {"stock": "AAPL", "price": 343.0},
        {"stock": "MSFT", "price": 500.0},
    ]

    with (
        patch("src.views.get_currency_rates", return_value=rates) as mock_rates,
        patch("src.views.get_stock_prices", return_value=prices) as mock_prices,
    ):
        result = json.loads(build_home_page("2021-12-20 12:00:00", transactions, settings))

    assert result["greeting"] == "Добрый день"
    assert result["cards"] == [
        {"last_digits": "1234", "total_spent": 175.0, "cashback": 1.75},
        {"last_digits": "9876", "total_spent": 10.0, "cashback": 0.1},
    ]
    assert [item["amount"] for item in result["top_transactions"]] == [
        200.0,
        -10.0,
        -25.0,
        -50.0,
        -100.0,
    ]
    assert result["currency_rates"] == rates
    assert result["stock_prices"] == prices
    mock_rates.assert_called_once_with(["USD", "EUR"])
    mock_prices.assert_called_once_with(["AAPL", "MSFT"])


def test_main_page_reads_project_files() -> None:
    with (
        patch(
            "src.views.get_currency_rates",
            side_effect=lambda currencies: [{"currency": currency, "rate": 1.0} for currency in currencies],
        ),
        patch(
            "src.views.get_stock_prices",
            side_effect=lambda stocks: [{"stock": stock, "price": 1.0} for stock in stocks],
        ),
    ):
        result = json.loads(main_page("2021-12-31 23:59:59"))

    assert result["greeting"] == "Доброй ночи"
    assert len(result["cards"]) >= 1
    assert len(result["top_transactions"]) == 5
    assert [item["currency"] for item in result["currency_rates"]] == ["USD", "EUR"]
    assert [item["stock"] for item in result["stock_prices"]] == ["AAPL", "AMZN", "GOOGL", "MSFT", "TSLA"]


def test_get_cards_info_skips_foreign_currency() -> None:
    transactions = pd.DataFrame(
        [
            {"Номер карты": "*1234", "Статус": "OK", "Сумма платежа": -100.0, "Валюта платежа": "RUB"},
            {"Номер карты": "*1234", "Статус": "OK", "Сумма платежа": -50.0, "Валюта платежа": "CNY"},
        ]
    )

    assert get_cards_info(transactions) == [{"last_digits": "1234", "total_spent": 100.0, "cashback": 1.0}]


def test_get_top_transactions_skips_foreign_currency() -> None:
    transactions = pd.DataFrame(
        {
            "Дата операции": pd.to_datetime(["2021-12-01", "2021-12-01"]),
            "Статус": ["OK", "OK"],
            "Сумма платежа": [100, 999],
            "Валюта платежа": ["RUB", "CNY"],
            "Категория": ["Покупки", "Покупки"],
            "Описание": ["рублёвая", "валютная"],
        }
    )

    result = get_top_transactions(transactions)

    assert [item["amount"] for item in result] == [100.0]
