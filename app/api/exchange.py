from fastapi import APIRouter, Query, status
from fastapi.responses import JSONResponse
from typing import Annotated
import math
import requests

router = APIRouter()


@router.get("/exchange_rates/")
def get_exchange_rates(
    from_currency: Annotated[
        str | None,
        Query(
            description="3 Characters ISO Currency Code"
        ),
    ] = "USD",
    to_currency: Annotated[
        str | None,
        Query(
            description="3 Characters ISO Currency Code"
        ),
    ] = "CAD",
    start_date: Annotated[
        str | None,
        Query(
            description="Start date range for Exchange Rate (format YYYY-MM-DD)"
        ),
    ] = "2023-08-01",
    end_date: Annotated[
        str | None,
        Query(
            description="End date range for Exchange Rate (format YYYY-MM-DD)"
        ),
    ] = "2023-08-31",
):
    return fetch_exchange_rates(from_currency, to_currency, start_date, end_date)


def fetch_exchange_rates(
    from_currency: str = "USD",
    to_currency: str = "CAD",
    start_date: str = "2023-08-01",
    end_date: str = "2023-08-31",
):
    # Construct the API request URL using the provided parameters
    base_url = "https://www.bankofcanada.ca/valet/observations/"
    serie_name = f"FX{from_currency}{to_currency}"
    api_url = f"{base_url}{serie_name}?start_date={start_date}&end_date={end_date}"

    try:
        # Make an HTTP GET request to the Bank of Canada API
        response = requests.get(api_url)

        # Check if the response status code is successful (200 OK)
        if response.status_code == 200:
            # Parse the JSON response to extract the CAD to USD exchange rate
            data = response.json()
            exchange_rate = {}
            for observation in data['observations']:
                if observation['d'] >= start_date and observation['d'] <= end_date:
                    exchange_rate[str(observation['d'])] = float(
                        observation[f'{serie_name}']['v'])

            if len(exchange_rate) > 0:
                return JSONResponse(
                    status_code=status.HTTP_200_OK,
                    content={
                        "serie_name": serie_name,
                        "exchange_rate": exchange_rate
                    }
                )
            else:
                return JSONResponse(
                    status_code=status.HTTP_404_NOT_FOUND,
                    content={
                        "error": "Exchange rate data not found for the specified date range."
                    }
                )
        else:
            return JSONResponse(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                content={
                    "error": f"Failed to fetch data from the Bank of Canada API. Status code: {response.status_code}"
                }
            )
    except Exception as e:
        print(str(e))
        return JSONResponse(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            content={"error": str(e)}
        )
