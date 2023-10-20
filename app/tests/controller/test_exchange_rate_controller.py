"""
test_exchange_rate_controller.py

This module contains tests for the exchange_rate_controller module. It tests the behavior of the API endpoint
by mocking the service layer and checking the responses from the controller.
"""

import os
from unittest.mock import patch

# Set the environment variable for testing purposes.
os.environ["ENV"] = "development"

# Now, import the app after setting the environment variable.
from app.main import app
from fastapi.testclient import TestClient

# Initialize a test client for the FastAPI application.
client = TestClient(app)

def mock_fetch_exchange_rates_success(*args, **kwargs):
    """
    Mock function to simulate a successful fetch of exchange rates from the service layer.

    Returns:
        tuple: A tuple containing exchange rate data and None for the error.
    """
    return {'2023-08-01': 1.25, '2023-08-02': 1.26}, None


def mock_fetch_exchange_rates_failure(*args, **kwargs):
    """
    Mock function to simulate a failure in fetching exchange rates from the service layer.

    Returns:
        tuple: A tuple containing None for the exchange rate data and an error message.
    """
    return None, "Some error occurred"


def test_get_exchange_rates_success():
    """
    Test the /exchange_rates/ endpoint for a successful response.
    
    The service layer is mocked to return a successful response. The test then checks if the API endpoint
    returns the expected status code and JSON response.
    """
    with patch('app.api.service.exchange_rate_service.ExchangeRateService.fetch_exchange_rates', new=mock_fetch_exchange_rates_success):
        response = client.get("/exchange-api/v1/exchange-rates/")
        assert response.status_code == 200
        assert response.json() == {
            "serie_name": "FXUSDCAD",
            "exchange_rate": {'2023-08-01': 1.25, '2023-08-02': 1.26}
        }


def test_get_exchange_rates_failure():
    """
    Test the /exchange_rates/ endpoint for a failure scenario.
    
    The service layer is mocked to return an error. The test then checks if the API endpoint
    returns the expected status code and error message in the JSON response.
    """
    with patch('app.api.service.exchange_rate_service.ExchangeRateService.fetch_exchange_rates', new=mock_fetch_exchange_rates_failure):
        response = client.get("/exchange-api/v1/exchange-rates/")
        assert response.status_code == 500
        assert response.json() == {"error": "Some error occurred"}
