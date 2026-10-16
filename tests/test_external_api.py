from unittest.mock import Mock, patch

from src.external_api import convert_to_rub


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