import pandas as pd

from backtest import Strategy
from backtest.indicators import SMA


def std_3(arr, n):
    return pd.Series(arr).rolling(n).std() * 3


class MeanReversion(Strategy):
    roll = 50

    def init(self):
        self.he = self.data.close

        self.he_mean = self.I(SMA, self.he, self.roll)
        self.he_std = self.I(std_3, self.he, self.roll)
        self.he_upper = self.he_mean + self.he_std
        self.he_lower = self.he_mean - self.he_std

        self.he_close = self.I(SMA, self.he, 1)

    def next(self):
        if self.he_close < self.he_lower:
            self.buy(tp=self.he_mean)
        if self.he_close > self.he_upper:
            self.sell(tp=self.he_mean)
