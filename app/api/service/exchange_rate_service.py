import math
import requests


class ExchangeRateService:
    """
    Service class responsible for fetching exchange rate data from the Bank of Canada API.
    """

    @staticmethod
    def fetch_exchange_rates(
        from_currency: str = "USD",
        to_currency: str = "CAD",
        start_date: str = "2023-08-01",
        end_date: str = "2023-08-31",
    ) -> (dict, str):
        """
        Fetch exchange rates for a given currency pair and date range.

        Args:
            from_currency (str, optional): The source currency for the exchange rate. Defaults to "USD".
            to_currency (str, optional): The target currency for the exchange rate. Defaults to "CAD".
            start_date (str, optional): The start date for the exchange rate data range. Defaults to "2023-08-01".
            end_date (str, optional): The end date for the exchange rate data range. Defaults to "2023-08-31".

        Returns:
            tuple: A tuple containing two elements:
                - dict: A dictionary with dates as keys and exchange rates as values.
                - str: An error message if there was an issue fetching the data, otherwise None.
        """

        # Construct the API request URL using the provided parameters.
        base_url = "https://www.bankofcanada.ca/valet/observations/"
        serie_name = f"FX{from_currency}{to_currency}"
        api_url = f"{base_url}{serie_name}?start_date={start_date}&end_date={end_date}"

        try:
            # Make an HTTP GET request to the Bank of Canada API.
            response = requests.get(api_url)

            # Check if the response status code is successful (200 OK).
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
