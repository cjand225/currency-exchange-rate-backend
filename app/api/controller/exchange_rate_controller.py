"""
exchange_rate_controller.py

This module defines the API endpoints related to exchange rates. It uses the ExchangeRateService
to fetch exchange rate data and provides an endpoint to retrieve exchange rates based on given parameters.
"""

from fastapi import APIRouter, Query, status
from fastapi.responses import JSONResponse
from typing import Annotated
from app.api.service.exchange_rate_service import ExchangeRateService

# Create a new router instance for the exchange rate endpoints.
router = APIRouter()


@router.get("/exchange-rates/")
def get_exchange_rates(
    from_currency: Annotated[
        str | None,
        Query(description="3 Characters ISO Currency Code"),
    ] = "USD",
    to_currency: Annotated[
        str | None,
        Query(description="3 Characters ISO Currency Code"),
    ] = "CAD",
    start_date: Annotated[
        str | None,
        Query(description="Start date range for Exchange Rate (format YYYY-MM-DD)"),
    ] = "2023-08-01",
    end_date: Annotated[
        str | None,
        Query(description="End date range for Exchange Rate (format YYYY-MM-DD)"),
    ] = "2023-08-31",
) -> JSONResponse:
    """
    Fetch exchange rates based on the provided parameters.

    Args:
        from_currency (str, optional): The source currency for the exchange rate. Defaults to "USD".
        to_currency (str, optional): The target currency for the exchange rate. Defaults to "CAD".
        start_date (str, optional): The start date for the exchange rate data range. Defaults to "2023-08-01".
        end_date (str, optional): The end date for the exchange rate data range. Defaults to "2023-08-31".

    Returns:
        JSONResponse: A JSON response containing the exchange rate data or an error message.
    """

    # Fetch exchange rate data using the ExchangeRateService.
    exchange_rate, error = ExchangeRateService.fetch_exchange_rates(
        from_currency, to_currency, start_date, end_date)

    # Handle potential errors from the service.
    if error:
        return JSONResponse(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            content={"error": error}
        )

    # Return the exchange rate data if available.
    if len(exchange_rate) > 0:
        return JSONResponse(
            status_code=status.HTTP_200_OK,
            content={
                "serie_name": f"FX{from_currency}{to_currency}",
                "exchange_rate": exchange_rate
            }
        )
    # Handle the case where no exchange rate data is found for the given date range.
    else:
        return JSONResponse(
            status_code=status.HTTP_404_NOT_FOUND,
            content={
                "error": "Exchange rate data not found for the specified date range."
            }
        )
