def filter_by_currency(transactions: list, currency: str):
    """Генератор, который возвращает только транзакции с указанной валютой"""
    for transaction in transactions:
        if transaction["operationAmount"]["currency"]["code"] == currency:
            yield transaction


def transaction_descriptions(transactions: list):
    """Генератор, который возвращает описания всех транзакций"""
    for transaction in transactions:
        yield transaction["description"]


def card_number_generator(start: int, stop: int):
    """Генератор, который возвращает номера карт в заданном диапазоне"""
    for i in range(start, stop + 1):
        digits = f"{i:016d}"
        yield (f"{digits[:4]} {digits[4:8]} " f"{digits[8:12]} {digits[12:16]}")
