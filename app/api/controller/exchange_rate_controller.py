from fastapi import APIRouter, Query, status
from fastapi.responses import JSONResponse
from typing import Annotated
from app.api.service.exchange_rate_service import ExchangeRateService

router = APIRouter()


@router.get("/exchange_rates/")
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
):
    exchange_rate, error = ExchangeRateService.fetch_exchange_rates(
        from_currency, to_currency, start_date, end_date)

    if error:
        return JSONResponse(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            content={"error": error}
        )

    if len(exchange_rate) > 0:
        return JSONResponse(
            status_code=status.HTTP_200_OK,
            content={
                "serie_name": f"FX{from_currency}{to_currency}",
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
