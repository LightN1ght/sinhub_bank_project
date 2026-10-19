from datetime import datetime

import pandas as pd
import pytest

from src.views import get_greeting, select_month_transactions


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