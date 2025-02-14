# indicators/Indicators.py
from .rsi import rsi
from .macd import macd

class Indicators:
    @staticmethod
    def getRSI(series, window=14):
        return rsi(series, window, last_only=True)

    @staticmethod
    def getMACD(series, fast_window=12, slow_window=26, signal_window=9):
        return macd(series, fast_window, slow_window, signal_window)
