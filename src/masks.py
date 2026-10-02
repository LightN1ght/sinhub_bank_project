def get_mask_card_number(user_card_number: str) -> str:
    """Функция которая маскирует номер карты пользователя"""
    if not user_card_number.strip():
        raise ValueError("Номер карты не должен быть пустым")
    return f"{user_card_number[:4]} {user_card_number[4:6]}** **** {user_card_number[-4:]}"


def get_mask_account(user_account_number: str) -> str:
    """Маскирует номер счёта, оставляя последние четыре символа."""
    account_number = user_account_number.strip()

    if len(account_number) < 4:
        raise ValueError("Номер счёта должен содержать не менее 4 символов")

    return "**" + account_number[-4:]
