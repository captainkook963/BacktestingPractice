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
        self.daily_rsi = self.I(ta.rsiI, pd.Series(self.data.Close), self.rsi_window)

        # This magical function does all the resampling 
        self.weekly_rsi = resample_apply(
            'W-FRI', ta.rsi, pd.Series(self.data.Close), self.rsi_window)


    def next(self):

        if (crossover(self.daily_rsi, self.upper_bound) and
                self.weekly_rsi[-1] > self.upper_bound):
            self.position.close()

        elif (crossover(self.lower_bound, self.daily_rsi) and
                self.lower_bound > self.weekly_rsi[-1]):
            self.buy()



bt = Backtest(GOOG, RsiOscillator, cash=10_000, commission=.002)
stats = bt.run()
bt.plot()