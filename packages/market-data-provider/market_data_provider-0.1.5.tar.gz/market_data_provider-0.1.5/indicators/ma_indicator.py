from typing import Dict

from indicators.indicator_interface import IndicatorInterface


class MovingAverageIndicator(IndicatorInterface):
    def __init__(self, name: str, window_length: int):
        self.window_length = window_length
        self.name = name
        self.window = []

    def get_name(self) -> str:
        return self.name

    def get_window_length(self) -> int:
        return self.window_length

    def apply(self, candle: Dict) -> float:
        self.window.append(candle['c'])
        if len(self.window) > self.window_length:
            self.window.pop(0)
        avg = sum(self.window) / len(self.window)
        return avg
