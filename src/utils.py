import json


def load_transactions(file_path):
    """Функция, которая загружает все транзакции из указанного файла"""
    try:
        with open(file_path, encoding="utf-8") as f:
            data = json.load(f)
    except FileNotFoundError:
        return []
    except json.JSONDecodeError:
        return []

    if not isinstance(data, list):
        return []

    return data
