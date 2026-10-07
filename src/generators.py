def filter_by_currency(transactions: list, currency: str):
    for transaction in transactions:
        if transaction["operationAmount"]["currency"]["code"] == currency:
            yield transaction


def transaction_descriptions(transactions: list):
    for transaction in transactions:
        yield transaction["description"]

def card_number_generator(min_range: int, max_range: int):
    for i in range(min_range, max_range+1):
        digits = f"{i:016d}"
        yield (
            f"{digits[:4]} {digits[4:8]} "
            f"{digits[8:12]} {digits[12:16]}"
        )

