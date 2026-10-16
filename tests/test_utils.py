from unittest.mock import mock_open, patch

from src.utils import load_transactions


def test_load_transactions_returns_list():
    fake_file = mock_open(read_data='[{"id": 1}]')

    with patch("builtins.open", fake_file):
        result = load_transactions("fake.json")

    assert result == [{"id": 1}]


def test_load_transactions_returns_empty_list_for_empty_file():
    fake_file = mock_open(read_data="")

    with patch("builtins.open", fake_file):
        result = load_transactions("fake.json")

    assert result == []


def test_load_transactions_returns_empty_list_for_non_list_json():
    fake_file = mock_open(read_data='{"id": 1}')

    with patch("builtins.open", fake_file):
        result = load_transactions("fake.json")

    assert result == []


def test_load_transactions_returns_empty_list_for_missing_file():
    with patch("builtins.open", side_effect=FileNotFoundError):
        result = load_transactions("missing.json")

    assert result == []


def test_load_transactions_returns_empty_list_for_invalid_json():
    fake_file = mock_open(read_data='[{"id": 1}')

    with patch("builtins.open", fake_file):
        result = load_transactions("fake.json")

    assert result == []
