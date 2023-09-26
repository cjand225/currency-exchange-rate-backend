from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)


def test_get_exchange_rates():
    # Define test input data (ExchangeRequest model)
    test_input = {
        "from_currency": "USD",
        "to_currency": "CAD",
        "start_date": "2023-08-01",
        "end_date": "2023-08-31",
        "serie_name": "FXUSDCAD"
    }

    # Make a request to the endpoint
    response = client.get("/exchange_rates/", params=test_input)

    # Assert response status code (200 OK in this case)
    assert response.status_code == 200

    expected_response = {
        "serie_name": "FXUSDCAD",
        "exchange_rate": 1.3291
    }

    assert response.json() == expected_response
