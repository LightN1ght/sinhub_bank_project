from unittest.mock import Mock, patch

from src.transaction_readers import (read_transactions_from_csv,
                                     read_transactions_from_excel)


def test_read_transactions_from_csv():
    expected = [{"id": 1, "state": "EXECUTED"}]
    fake_table = Mock()
    fake_table.to_dict.return_value = expected

    with patch(
        "src.transaction_readers.pd.read_csv",
        return_value=fake_table,
    ) as mock_read_csv:
        result = read_transactions_from_csv("fake.csv")

    assert result == expected
    mock_read_csv.assert_called_once_with("fake.csv", sep=";")
    fake_table.to_dict.assert_called_once_with(orient="records")


def test_read_transactions_from_excel():
    expected = [{"id": 2, "state": "CANCELED"}]
    fake_table = Mock()
    fake_table.to_dict.return_value = expected

    with patch(
        "src.transaction_readers.pd.read_excel",
        return_value=fake_table,
    ) as mock_read_excel:
        result = read_transactions_from_excel("fake.xlsx")

    assert result == expected
    mock_read_excel.assert_called_once_with("fake.xlsx")
    fake_table.to_dict.assert_called_once_with(orient="records")
