import math
import requests


class ExchangeRateService:

    @staticmethod
    def fetch_exchange_rates(
        from_currency: str = "USD",
        to_currency: str = "CAD",
        start_date: str = "2023-08-01",
        end_date: str = "2023-08-31",
    ):
        base_url = "https://www.bankofcanada.ca/valet/observations/"
        serie_name = f"FX{from_currency}{to_currency}"
        api_url = f"{base_url}{serie_name}?start_date={start_date}&end_date={end_date}"

        try:
            response = requests.get(api_url)
            if response.status_code == 200:
                data = response.json()
                exchange_rate = {}
                for observation in data['observations']:
                    if observation['d'] >= start_date and observation['d'] <= end_date:
                        exchange_rate[str(observation['d'])] = math.ceil(
                            float(observation[f'{serie_name}']['v']) * 100.0) / 100.0

                return exchange_rate, None
            else:
                return None, f"Failed to fetch data. Status code: {response.status_code}"
        except Exception as e:
            return None, str(e)
