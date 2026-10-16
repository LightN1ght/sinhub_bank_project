import json

def load_transactions(file_path):
    try:
        with open(file_path, encoding='utf-8') as f:
            data = json.load(f)
    except FileNotFoundError:
        return []
    except json.JSONDecodeError:
        return []

    if type(data) != list:
        return []

    return data
