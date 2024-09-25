from backtest import Strategy
from backtest.lib import crossover
from backtest.indicators import SMA


class SmaCross(Strategy):
    n1: int
    n2: int
    order_size: float = 0.5

    def init(self):
        close = self.data.close
        self.sma1 = self.I(SMA, close, self.n1)
        self.sma2 = self.I(SMA, close, self.n2)

    def next(self):
        if crossover(self.sma1, self.sma2):
            self.buy(size=self.order_size)
        elif crossover(self.sma2, self.sma1):
            self.sell(size=self.order_size)
