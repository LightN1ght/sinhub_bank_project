def get_mask_card_number(user_card_number: str) -> str:
    """Функция которая маскирует номер карты пользователя"""
    return f"{user_card_number[:4]} {user_card_number[4:6]}** **** {user_card_number[-4:]}"


def get_mask_account(user_account_number: str) -> str:
    """Функция которая маскирует номер счёта пользователя"""
    return "**" + user_account_number[-4:]
