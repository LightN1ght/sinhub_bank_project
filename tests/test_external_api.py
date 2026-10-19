from unittest.mock import Mock, call, patch

import pytest

from src.external_api import convert_to_rub, get_currency_rates, get_stock_prices


def make_transaction(amount, currency_code):
    return {
        "operationAmount": {
            "amount": amount,
            "currency": {
                "code": currency_code,
            },
        },
    }


def test_convert_to_rub_returns_rub_amount_without_api_request():
    transaction = make_transaction("120.50", "RUB")

    with patch("src.external_api.requests.request") as mock_request:
        result = convert_to_rub(transaction)

    assert result == 120.50
    assert isinstance(result, float)
    mock_request.assert_not_called()


def test_convert_to_rub_converts_usd():
    transaction = make_transaction("10", "USD")
    fake_response = Mock()
    fake_response.json.return_value = {"result": 900.5}

    with patch("src.external_api.EXCHANGE_API", "test-api-key"):
        with patch("src.external_api.requests.request") as mock_request:
            mock_request.return_value = fake_response
            result = convert_to_rub(transaction)

    assert result == 900.5
    assert isinstance(result, float)
    fake_response.raise_for_status.assert_called_once_with()
    mock_request.assert_called_once()

    request_args = mock_request.call_args
    assert request_args.args[0] == "GET"
    assert "from=USD" in request_args.args[1]
    assert "to=RUB" in request_args.args[1]
    assert request_args.kwargs["headers"] == {"apikey": "test-api-key"}


def test_convert_to_rub_converts_eur():
    transaction = make_transaction("10", "EUR")
    fake_response = Mock()
    fake_response.json.return_value = {"result": 950.75}

    with patch("src.external_api.EXCHANGE_API", "test-api-key"):
        with patch("src.external_api.requests.request") as mock_request:
            mock_request.return_value = fake_response
            result = convert_to_rub(transaction)

    assert result == 950.75
    assert isinstance(result, float)
    fake_response.raise_for_status.assert_called_once_with()
    mock_request.assert_called_once()

    request_args = mock_request.call_args
    assert request_args.args[0] == "GET"
    assert "from=EUR" in request_args.args[1]
    assert "to=RUB" in request_args.args[1]
    assert request_args.kwargs["headers"] == {"apikey": "test-api-key"}


def test_get_currency_rates():
    fake_response = Mock()
    fake_response.json.return_value = {
        "success": True,
        "rates": {"RUB": 100.0, "USD": 2.0},
    }

    with patch("src.external_api.EXCHANGE_API", "test-api-key"):
        with patch("src.external_api.requests.get") as mock_get:
            mock_get.return_value = fake_response
            result = get_currency_rates(["USD", "EUR"])

    assert result == [
        {"currency": "USD", "rate": 50.0},
        {"currency": "EUR", "rate": 100.0},
    ]
    fake_response.raise_for_status.assert_called_once_with()
    mock_get.assert_called_once_with(
        "https://api.apilayer.com/exchangerates_data/latest",
        params={"base": "EUR", "symbols": "EUR,RUB,USD"},
        headers={"apikey": "test-api-key"},
        timeout=10,
    )


def test_get_stock_prices():
    apple_response = Mock()
    apple_response.json.return_value = {"price": "200.99"}

    microsoft_response = Mock()
    microsoft_response.json.return_value = {"price": "415.50"}

    with patch("src.external_api.TWELVE_DATA_API", "test-key"):
        with patch(
            "src.external_api.requests.get",
            side_effect=[apple_response, microsoft_response],
        ) as mock_get:
            result = get_stock_prices(["AAPL", "MSFT"])

    assert result == [
        {"stock": "AAPL", "price": 200.99},
        {"stock": "MSFT", "price": 415.50},
    ]
    assert mock_get.call_args_list == [
        call(
            "https://api.twelvedata.com/price",
            params={"symbol": "AAPL"},
            headers={"Authorization": "apikey test-key"},
            timeout=10,
        ),
        call(
            "https://api.twelvedata.com/price",
            params={"symbol": "MSFT"},
            headers={"Authorization": "apikey test-key"},
            timeout=10,
        ),
    ]


def test_get_stock_prices_handles_api_error():
    error_response = Mock()
    error_response.json.return_value = {
        "status": "error",
        "message": "API limit reached",
    }

    with patch("src.external_api.TWELVE_DATA_API", "test-key"):
        with patch("src.external_api.requests.get", return_value=error_response):
            with pytest.raises(RuntimeError, match="AAPL"):
                get_stock_prices(["AAPL"])
