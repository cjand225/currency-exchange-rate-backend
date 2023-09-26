from fastapi import APIRouter, Query
import requests

router = APIRouter()


@router.get("/exchange_rates/")
def get_exchange_rates():
    pass


def fetch_exchange_rates():
    pass
