import datetime
import pandas_ta as ta
import pandas as pd
from backtesting import Backtest
from backtesting import Strategy
from backtesting.lib import crossover
from backtesting.test import GOOG


class RsiOscillator(Strategy):
    upper_bound = 70
    lower_bound = 30
    rsi_window = 14

    # All initial calculations
    def init(self):
        self.daily_rsi = self.I(ta.rsi, pd.Series(self.data.Close), self.rsi_window)

    def next(self):

        price = self.data.Close[-1]

        if crossover(self.daily_rsi, self.upper_bound):
            self.position.close()

        elif self.lower_bound > self.daily_rsi[-1]:
            self.buy(size=1) # number of shares
            #self.buy(size=0.1) # percentage of cash available



bt = Backtest(GOOG, RsiOscillator, cash=10_000, commission=.002)
stats = bt.run()
bt.plot()