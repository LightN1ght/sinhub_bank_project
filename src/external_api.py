import os

import requests
from dotenv import load_dotenv

load_dotenv()
EXCHANGE_API = os.getenv("EXCHANGE_API")


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
