import logging
from pathlib import Path

logs_dir = Path(__file__).resolve().parent.parent / "logs"
logs_dir.mkdir(parents=True, exist_ok=True)

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

if not logger.handlers:
    file_handler = logging.FileHandler(
        logs_dir / "masks.log",
        mode="w",
        encoding="utf-8",
    )
    file_formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")
    file_handler.setFormatter(file_formatter)
    logger.addHandler(file_handler)


def get_mask_card_number(user_card_number: str) -> str:
    """Функция, которая маскирует номер карты пользователя"""
    if not user_card_number.strip():
        logger.error("Введённый номер карты пуст")
        raise ValueError("Номер карты не должен быть пустым")
    logger.debug("Номер карты отформатирован")
    return f"{user_card_number[:4]} {user_card_number[4:6]}** **** {user_card_number[-4:]}"


def get_mask_account(user_account_number: str) -> str:
    """Маскирует номер счёта, оставляя последние четыре символа."""
    account_number = user_account_number.strip()

    if len(account_number) < 4:
        logger.error("Номер счёта содержит менее 4 символов")
        raise ValueError("Номер счёта должен содержать не менее 4 символов")

    logger.debug("Номер счёта замаскирован")
    return "**" + account_number[-4:]
