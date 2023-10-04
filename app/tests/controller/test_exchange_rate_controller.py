from app.main import app
from fastapi.testclient import TestClient
from unittest.mock import patch

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
