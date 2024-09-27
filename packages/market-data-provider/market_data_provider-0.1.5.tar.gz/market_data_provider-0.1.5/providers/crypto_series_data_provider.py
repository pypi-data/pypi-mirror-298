from datetime import datetime
from typing import List, Dict

from .common import generate_date_range
from .crypto_ohlc_provider import CryptoOhlcProvider
from .crypto_trades_provider import CryptoTradesProvider
from indicators.indicator_interface import IndicatorInterface


class CryptoSeriesDataProvider:
    def __init__(self, instruments: List[str], day_from: datetime, day_to: datetime,
                 interval: int = 1, indicators: List[IndicatorInterface] = None):
        self.interval = interval
        self.selected_days = generate_date_range(day_from, day_to)
        self.ohlc_data = {instrument: [] for instrument in instruments}
        self.indicators = indicators

    def _populate_ohlc_series(self) -> None:
        for instrument in self.ohlc_data:
            series_data = []
            for target_day in self.selected_days:
                ohlc_series = CryptoOhlcProvider(target_day, instrument, self.interval).get_ohlc_series()
                intervals = [ohlc['t'] for ohlc in ohlc_series]
                grouped_trades = CryptoTradesProvider(target_day, instrument).get_grouped_trades(intervals)

                for candle in ohlc_series:
                    candle['trades'] = grouped_trades.get(candle['t'], [])

                series_data.extend(ohlc_series)
            series_data = sorted(series_data, key=lambda x: x['t'])

            if self.indicators:
                for i, candle in enumerate(series_data):
                    for indicator in self.indicators:
                        window_length = indicator.get_window_length()

                        if i + 1 >= window_length:
                            indicator_value = indicator.apply(candle)
                        else:
                            indicator_value = None
                        candle[indicator.get_name()] = indicator_value

            series_data = [candle for candle in series_data if all(value is not None for value in candle.values())]
            self.ohlc_data[instrument] = sorted(series_data, key=lambda x: x['t'])

    def get_series(self, instrument: str) -> List[Dict]:
        if not any(self.ohlc_data[instrument] for instrument in self.ohlc_data):
            self._populate_ohlc_series()

        ohlc_series = self.ohlc_data.get(instrument)
        return ohlc_series
