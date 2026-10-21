import pytest

from src.masks import get_mask_account, get_mask_card_number


@pytest.mark.parametrize(
    ("card_number", "expected"),
    [
        ("1234567812345678", "1234 56** **** 5678"),
        ("12345678", "1234 56** **** 5678"),
        ("123456789012", "1234 56** **** 9012"),
        ("1234567890123456789", "1234 56** **** 6789"),
    ],
)
def test_get_mask_number(card_number, expected):
    assert get_mask_card_number(card_number) == expected


def test_get_mask_card_number_rejects_empty_string():
    with pytest.raises(ValueError):
        get_mask_card_number("")


@pytest.mark.parametrize(
    ("account_number", "expected"),
    [
        ("40817810099910004321", "**4321"),
        ("1234", "**1234"),
    ],
)
def test_get_mask_account(account_number, expected):
    assert get_mask_account(account_number) == expected


@pytest.mark.parametrize("account_number", ["", " ", "    ", "\t\n", "1", "12", "123"])
def test_get_mask_account_rejects_short_number(account_number):
    with pytest.raises(ValueError):
        get_mask_account(account_number)
