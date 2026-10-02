from src import masks
from datetime import datetime


def mask_account_card(user_account: str) -> str:
    """Функция, которая маскирует карту или счёт пользователя и создаёт виджет"""
    parts = user_account.split()
    if len(parts) < 2:
        raise ValueError("Нужно указать тип карты или счёта и номер")

    account_type = " ".join(parts[:-1])
    account_number = parts[-1]

    if account_type == "Счет":
        masked_card = masks.get_mask_account(account_number)
    else:
        masked_card = masks.get_mask_card_number(account_number)

    return f"{account_type} {masked_card}"


def get_date(date: str) -> str:
    """Функция, которая обрабатывает формат даты"""
    return datetime.fromisoformat(date).strftime("%d.%m.%Y")