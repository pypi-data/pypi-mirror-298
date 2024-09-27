import datetime
import os
from datetime import datetime
from typing import Dict, List

import requests
from requests.exceptions import ConnectionError, Timeout, HTTPError, RequestException
from tenacity import retry, stop_after_attempt, wait_fixed, retry_if_exception_type


class CryptoTradesProvider:
    def __init__(self, selected_date: datetime, instrument: str):
        self.api_token = os.getenv('POLYGON_API_TOKEN')
        if not self.api_token:
            raise EnvironmentError(
                "POLYGON_API_TOKEN is required to access the API. Please set the environment variable.")
        self.selected_date = selected_date
        self.instrument = instrument

    @staticmethod
    def _map_trades(trades_data) -> List[Dict[str, str]]:
        return [
            {
                'datetime': datetime.utcfromtimestamp(trade['participant_timestamp'] / 1e9).strftime(
                    "%Y-%m-%d %H:%M:%S"),
                't': trade['participant_timestamp'],
                'p': trade['price'],
                's': trade['size'],
                'c': "s" if 1 in trade['conditions'] else "b" if 2 in trade['conditions'] else "unknown"
            }
            for trade in trades_data
        ]

    @retry(stop=stop_after_attempt(15), wait=wait_fixed(10),
           retry=retry_if_exception_type((ConnectionError, Timeout, HTTPError, RequestException)))
    def _download_trades(self):
        formatted_date = self.selected_date.strftime("%Y-%m-%d")
        print(f'Trades: {self.instrument} {formatted_date}')
        url = f"https://api.polygon.io/v3/trades/{self.instrument}"
        params = {
            "timestamp": formatted_date,
            "limit": 50000,
            "apiKey": self.api_token
        }

        trades_data = []
        while url:
            response = requests.get(url, params=params)
            response.raise_for_status()
            data = response.json()
            trades_data.extend(data.get('results', []))
            url = data.get('next_url', None)
            params = {
                "apiKey": self.api_token
            }

        return trades_data

    def _get_trades(self) -> List[Dict[str, any]]:
        trades = self._download_trades()
        trades = self._map_trades(trades)
        trades = sorted(trades, key=lambda x: x['t'])

        return trades

    def get_grouped_trades(self, intervals):
        interval_length = intervals[1] - intervals[0]
        grouped_trades = {interval: [] for interval in intervals}

        for trade in self._get_trades():
            trade_time_ms = trade['t'] // 1000000
            interval_index = (trade_time_ms - intervals[0]) // interval_length

            if 0 <= interval_index < len(intervals):
                interval_start = intervals[interval_index]
                grouped_trades[interval_start].append(trade)

        return grouped_trades
