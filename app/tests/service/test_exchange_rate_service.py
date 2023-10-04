from app.api.service.exchange_rate_service import ExchangeRateService
from unittest.mock import patch


def successful_mock_response(*args, **kwargs):
    class MockResponse:
        status_code = 200

        @staticmethod
        def json():
            return {
                'observations': [
                    {'d': '2023-08-01', 'FXUSDCAD': {'v': '1.25'}},
                    {'d': '2023-08-02', 'FXUSDCAD': {'v': '1.26'}}
                ]
            }
    return MockResponse()


def failed_mock_response(*args, **kwargs):
    class MockResponse:
        status_code = 500
    return MockResponse()


def test_fetch_exchange_rates_success():
    with patch('requests.get', new=successful_mock_response):
        rates, error = ExchangeRateService.fetch_exchange_rates()
        assert error is None
        assert rates == {'2023-08-01': 1.25, '2023-08-02': 1.26}


def test_fetch_exchange_rates_failure():
    with patch('requests.get', new=failed_mock_response):
        rates, error = ExchangeRateService.fetch_exchange_rates()
        assert rates is None
        assert "Failed to fetch data. Status code: 500" in error
