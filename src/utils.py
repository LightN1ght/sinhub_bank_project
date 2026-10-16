import json
from pathlib import Path
import logging

logs_dir = Path(__file__).resolve().parent.parent / "logs"
logs_dir.mkdir(parents=True, exist_ok=True)

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

if not logger.handlers:
    file_handler = logging.FileHandler(
        logs_dir / "utils.log",
        mode="w",
        encoding="utf-8",
    )
    file_formatter = logging.Formatter(
        "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    )
    file_handler.setFormatter(file_formatter)
    logger.addHandler(file_handler)


def load_transactions(file_path):
    """Функция, которая загружает все транзакции из указанного файла"""
    try:
        with open(file_path, encoding="utf-8") as f:
            data = json.load(f)
    except FileNotFoundError:
        logger.error("Файл %s не найден", file_path)
        return []
    except json.JSONDecodeError as error:
        logger.error("Не удалось разобрать JSON-файл %s: %s", file_path, error)
        return []

    if not isinstance(data, list):
        logger.error("В файле %s ожидался список транзакций", file_path)
        return []

    logger.debug("Транзакции загружены")
    return data
