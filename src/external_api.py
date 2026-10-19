import math
import os

import requests
from dotenv import load_dotenv

load_dotenv()
EXCHANGE_API = os.getenv("EXCHANGE_API")
TWELVE_DATA_API = os.getenv("TWELVE_DATA_API")


def convert_to_rub(transaction):
    """Функция, которая конвертирует сумму операции в рубли, если нужно, и возвращает сумму в виде float"""
    transaction_currency_code = transaction["operationAmount"]["currency"]["code"]
    transaction_amount = transaction["operationAmount"]["amount"]
    if transaction_currency_code == "RUB":
        transaction_amount_converted = float(transaction_amount)
    elif transaction_currency_code in ("USD", "EUR"):
        url = (
            f"https://api.apilayer.com/exchangerates_data/convert"
            f"?to=RUB&from={transaction_currency_code}"
            f"&amount={transaction_amount}"
        )

        headers = {"apikey": EXCHANGE_API}

        api_response = requests.request("GET", url, headers=headers)
        api_response.raise_for_status()
        transaction_amount_converted = float(api_response.json()["result"])

    return transaction_amount_converted


def get_currency_rates(currencies: list[str]) -> list[dict[str, str | float]]:
    """Возвращает стоимость одной единицы каждой валюты в рублях."""
    if not currencies:
        return []
    if not EXCHANGE_API:
        raise ValueError("Не указан ключ Exchange Rates Data API")

    symbols = ",".join(sorted(set(currencies) | {"RUB"}))
    response = requests.get(
        "https://api.apilayer.com/exchangerates_data/latest",
        params={"base": "EUR", "symbols": symbols},
        headers={"apikey": EXCHANGE_API},
        timeout=10,
    )
    response.raise_for_status()
    data = response.json()

    if data.get("success") is False:
        raise RuntimeError("API не вернул курсы валют")

    rates = data["rates"]
    rub_per_eur = float(rates["RUB"])
    result: list[dict[str, str | float]] = []

    for currency in currencies:
        units_per_eur = 1.0 if currency == "EUR" else float(rates[currency])
        if units_per_eur <= 0:
            raise ValueError(f"Некорректный курс валюты {currency}")

        result.append(
            {
                "currency": currency,
                "rate": rub_per_eur / units_per_eur,
            }
        )

    return result


def get_stock_prices(stocks: list[str]) -> list[dict[str, str | float]]:
    """Возвращает последние доступные цены акций."""
    if not stocks:
        return []
    if not TWELVE_DATA_API:
        raise ValueError("Не указан ключ Twelve Data API")

    result: list[dict[str, str | float]] = []

    for stock in stocks:
        response = requests.get(
            "https://api.twelvedata.com/price",
            params={"symbol": stock},
            headers={"Authorization": f"apikey {TWELVE_DATA_API}"},
            timeout=10,
        )
        response.raise_for_status()
        data = response.json()

        if "price" not in data:
            raise RuntimeError(f"Не удалось получить цену акции {stock}")

        price = float(data["price"])
        if not math.isfinite(price) or price <= 0:
            raise ValueError(f"Некорректная цена акции {stock}")

        result.append({"stock": stock, "price": price})

    return result
