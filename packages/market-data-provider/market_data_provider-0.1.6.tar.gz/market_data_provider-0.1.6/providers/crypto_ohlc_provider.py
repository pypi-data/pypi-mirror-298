import datetime
import os
from datetime import datetime
from typing import Dict, List

import requests
from requests.exceptions import ConnectionError, Timeout, HTTPError, RequestException
from tenacity import retry, stop_after_attempt, wait_fixed, retry_if_exception_type


class CryptoOhlcProvider:
    def __init__(self, selected_date: datetime, instrument: str, interval: int, interval_type: str = 'minute'):
        self.api_token = os.getenv('POLYGON_API_TOKEN')
        if not self.api_token:
            raise EnvironmentError(
                "POLYGON_API_TOKEN is required to access the API. Please set the environment variable.")
        self.selected_date = selected_date
        self.instrument = instrument
        self.interval = interval
        self.interval_type = interval_type

    @retry(stop=stop_after_attempt(15), wait=wait_fixed(10),
           retry=retry_if_exception_type((ConnectionError, Timeout, HTTPError, RequestException)))
    def _download_ohlc_series(self) -> Dict:
        formatted_date = self.selected_date.strftime("%Y-%m-%d")
        print(f'OHLC: {self.instrument} {formatted_date}')
        url = (f"https://api.polygon.io/v2/aggs/ticker/{self.instrument}/range/{self.interval}/{self.interval_type}/"
               f"{formatted_date}/{formatted_date}?adjusted=true&sort=asc&limit=50000&apiKey={self.api_token}")
        response = requests.get(url)
        response.raise_for_status()
        return response.json().get('results', [])

    def _map_ohlc_series(self, ohlc_series) -> List[Dict[str, float]]:
        return [
            {
                'datetime': datetime.utcfromtimestamp(point['t'] / 1000.0).strftime("%Y-%m-%d %H:%M:%S"),
                't': point['t'],
                'o': point['o'],
                'h': point['h'],
                'l': point['l'],
                'c': point['c'],
                'v': point['v'],
                **({'n': point['n']} if 'n' in point else {})
            }
            for point in ohlc_series
        ]

    def get_ohlc_series(self) -> List[Dict[str, float]]:
        ohlc_series = self._download_ohlc_series()
        ohlc_series = self._map_ohlc_series(ohlc_series)

        return ohlc_series
