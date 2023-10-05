"""
test_exchange_rate_service.py

This module contains tests for the ExchangeRateService class. It tests the behavior of the service
by mocking external HTTP requests and checking the responses from the service methods.
"""

from app.api.service.exchange_rate_service import ExchangeRateService
from unittest.mock import patch

def successful_mock_response(*args, **kwargs):
    """
    Mock function to simulate a successful HTTP response from the Bank of Canada API.

    Returns:
        MockResponse: A mock object with a status code of 200 and a json method that returns
                      exchange rate data.
    """
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
    """
    Mock function to simulate a failed HTTP response from the Bank of Canada API.

    Returns:
        MockResponse: A mock object with a status code of 500.
    """
    class MockResponse:
        status_code = 500
    return MockResponse()

def test_fetch_exchange_rates_success():
    """
    Test the fetch_exchange_rates method for a successful response.
    
    The external HTTP request is mocked to return a successful response.
    """
    with patch('requests.get', new=successful_mock_response):
        rates, error = ExchangeRateService.fetch_exchange_rates()
        assert error is None
        assert rates == {'2023-08-01': 1.25, '2023-08-02': 1.26}

def test_fetch_exchange_rates_failure():
    """
    Test the fetch_exchange_rates method for a failure scenario.
    
    The external HTTP request is mocked to return an error.
    """
    with patch('requests.get', new=failed_mock_response):
        rates, error = ExchangeRateService.fetch_exchange_rates()
        assert rates is None
        assert "Failed to fetch data. Status code: 500" in error
