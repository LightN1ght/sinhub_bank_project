import pandas as pd

def read_transactions_from_csv(file_path):
    """Читает транзакции из CSV файла"""
    table = pd.read_csv(file_path, sep=";")
    return table.to_dict(orient="records")


def read_transactions_from_excel(file_path):
    """Читает транзакции из excel файла"""
    table = pd.read_excel(file_path)
    return table.to_dict(orient="records")
