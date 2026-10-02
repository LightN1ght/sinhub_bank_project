import pytest

from src.widget import mask_account_card, get_date


@pytest.mark.parametrize(
    ("value", "expected"),
    [
        (
            "Visa Platinum 1234567812345678",
            "Visa Platinum 1234 56** **** 5678",
        ),
        (
            "MasterCard 9876543210987654",
            "MasterCard 9876 54** **** 7654",
        ),
        (
            "Счет 40817810099910004321",
            "Счет **4321",
        ),
        (
            "Счет 1234",
            "Счет **1234",
        ),
        (
            "  Visa   Platinum  1234567812345678  ",
            "Visa Platinum 1234 56** **** 5678",
        ),
    ],
)
def test_mask_account_card(value, expected):
    assert mask_account_card(value) == expected

@pytest.mark.parametrize("value", ["", "   ", "Visa", "Счет"])
def test_mask_account_card_rejects_missing_number(value):
    with pytest.raises(ValueError):
        mask_account_card(value)

@pytest.mark.parametrize(
    ("value", "expected"),
    [
        ("2024-03-11T02:26:18.671407", "11.03.2024"),
        ("2024-03-11", "11.03.2024"),
        ("2000-01-01", "01.01.2000"),
    ],
)
def test_get_date(value, expected):
    assert get_date(value) == expected

@pytest.mark.parametrize("value", ["", "   ", "не дата", "2024-13-40"])
def test_get_date_rejects_invalid_input(value):
    with pytest.raises(ValueError):
        get_date(value)