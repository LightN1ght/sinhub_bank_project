from datetime import datetime

import pandas as pd


def get_greeting(current_time: datetime) -> str:
    """Возвращает приветствие по времени суток"""
    hour = current_time.hour

    if 6 <= hour < 12:
        return "Доброе утро"
    if 12 <= hour < 18:
        return "Добрый день"
    if 18 <= hour < 23:
        return "Добрый вечер"
    return "Доброй ночи"


def select_month_transactions(
    transactions: pd.DataFrame,
    date_time: str,
) -> pd.DataFrame:
    """Выбирает операции с начала месяца по указанную дату и время"""
    requested_at = datetime.strptime(date_time, "%Y-%m-%d %H:%M:%S")
    month_start = requested_at.replace(day=1, hour=0, minute=0, second=0)

    dates = transactions["Дата операции"]
    mask = (dates >= month_start) & (dates <= requested_at)
    return transactions.loc[mask]

def get_cards_info(transactions: pd.DataFrame) -> list[dict[str, str | float]]:
    """Считает рублёвые расходы и кешбэк по каждой карте."""
    expenses = transactions.loc[
        transactions["Статус"].eq("OK")
        & transactions["Сумма платежа"].lt(0)
        & transactions["Номер карты"].notna()
    ].copy()

    if expenses["Валюта платежа"].ne("RUB").any():
        raise ValueError("Для нерублёвых платежей нужна конвертация")

    expenses["last_digits"] = expenses["Номер карты"].astype(str).str[-4:]
    totals = expenses.groupby("last_digits", sort=True)["Сумма платежа"].sum()

    cards = []
    for last_digits, amount in totals.items():
        total_spent = round(-float(amount), 2)
        cards.append(
            {
                "last_digits": last_digits,
                "total_spent": total_spent,
                "cashback": round(total_spent / 100, 2),
            }
        )

    return cards