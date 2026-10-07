import pytest

from src.generators import (card_number_generator, filter_by_currency,
                            transaction_descriptions)


def test_filter_by_currency(transactions):
    result = list(filter_by_currency(transactions, "USD"))
    actual_ids = [transaction["id"] for transaction in result]
    assert actual_ids == [939719570, 142264268, 895315941]


def test_filter_by_currency_not_match(transactions):
    result = list(filter_by_currency(transactions, "EUR"))
    actual_ids = [transaction["id"] for transaction in result]
    assert actual_ids == []


def test_filter_by_currency_empty():
    result = list(filter_by_currency([], "USD"))
    assert result == []


def test_transaction_descriptions(transactions):
    actual = list(transaction_descriptions(transactions))
    expected = [
        "Перевод организации",
        "Перевод со счета на счет",
        "Перевод со счета на счет",
        "Перевод с карты на карту",
        "Перевод организации",
    ]
    assert actual == expected


def test_transaction_descriptions_empty():
    actual = list(transaction_descriptions([]))
    assert actual == []


def test_card_number_generator():
    actual = list(card_number_generator(1, 3))
    assert actual == [
        "0000 0000 0000 0001",
        "0000 0000 0000 0002",
        "0000 0000 0000 0003",
    ]


@pytest.mark.parametrize(
    ("min_range", "max_range", "expected"),
    [(0, 0, ["0000 0000 0000 0000"]), (10, 10, ["0000 0000 0000 0010"]), (5, 3, [])],
)
def test_card_number_generator_limits(min_range, max_range, expected):
    result = list(card_number_generator(min_range, max_range))
    assert result == expected
