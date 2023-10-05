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
    return {'2023-08-01': 1.25, '2023-08-02': 1.26}, None


def mock_fetch_exchange_rates_failure(*args, **kwargs):
    return None, "Some error occurred"


def test_get_exchange_rates_success():
    with patch('app.api.service.exchange_rate_service.ExchangeRateService.fetch_exchange_rates', new=mock_fetch_exchange_rates_success):
        response = client.get("/exchange_rates/")
        assert response.status_code == 200
        assert response.json() == {
            "serie_name": "FXUSDCAD",
            "exchange_rate": {'2023-08-01': 1.25, '2023-08-02': 1.26}
        }


def test_get_exchange_rates_failure():
    with patch('app.api.service.exchange_rate_service.ExchangeRateService.fetch_exchange_rates', new=mock_fetch_exchange_rates_failure):
        response = client.get("/exchange_rates/")
        assert response.status_code == 500
        assert response.json() == {"error": "Some error occurred"}
