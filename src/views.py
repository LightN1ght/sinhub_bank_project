import json
import logging
from datetime import datetime
from pathlib import Path

import pandas as pd

from src.external_api import get_currency_rates, get_stock_prices
from src.utils import load_operations

logger = logging.getLogger(__name__)


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
    """Считает рублёвые расходы и кешбэк по каждой карте"""
    expenses = transactions.loc[
        transactions["Статус"].eq("OK") & transactions["Сумма платежа"].lt(0) & transactions["Номер карты"].notna()
    ].copy()

    if expenses["Валюта платежа"].ne("RUB").any():
        raise ValueError("Для нерублёвых платежей нужна конвертация")

    expenses["last_digits"] = expenses["Номер карты"].astype(str).str[-4:]
    totals = expenses.groupby("last_digits", sort=True)["Сумма платежа"].sum()

    cards: list[dict[str, str | float]] = []
    for last_digits, amount in totals.items():
        total_spent = round(-float(amount), 2)
        cards.append(
            {
                "last_digits": str(last_digits),
                "total_spent": total_spent,
                "cashback": round(total_spent / 100, 2),
            }
        )

    return cards


def get_top_transactions(
    transactions: pd.DataFrame,
) -> list[dict[str, str | float]]:
    """Возвращает пять успешных операций по убыванию суммы платежа"""
    completed = transactions.loc[transactions["Статус"].eq("OK")]
    top_five = completed.nlargest(5, "Сумма платежа")

    result = []
    for _, row in top_five.iterrows():
        category = row["Категория"]
        result.append(
            {
                "date": row["Дата операции"].strftime("%d.%m.%Y"),
                "amount": float(row["Сумма платежа"]),
                "category": "" if pd.isna(category) else str(category),
                "description": str(row["Описание"]),
            }
        )

    return result


def build_home_page(
    date_time: str,
    transactions: pd.DataFrame,
    settings: dict[str, list[str]],
) -> str:
    """Собирает JSON главной страницы из переданных данных"""
    current_time = datetime.strptime(date_time, "%Y-%m-%d %H:%M:%S")
    month_transactions = select_month_transactions(transactions, date_time)

    response = {
        "greeting": get_greeting(current_time),
        "cards": get_cards_info(month_transactions),
        "top_transactions": get_top_transactions(month_transactions),
        "currency_rates": get_currency_rates(settings["user_currencies"]),
        "stock_prices": get_stock_prices(settings["user_stocks"]),
    }

    return json.dumps(response, ensure_ascii=False, allow_nan=False)


def main_page(date_time: str) -> str:
    """Загружает данные и возвращает JSON главной страницы."""
    project_root = Path(__file__).resolve().parent.parent
    transactions = load_operations(str(project_root / "data" / "operations.xlsx"))
    settings = json.loads((project_root / "user_settings.json").read_text(encoding="utf-8"))

    logger.info("Формирование главной страницы за %s", date_time)
    return build_home_page(date_time, transactions, settings)
