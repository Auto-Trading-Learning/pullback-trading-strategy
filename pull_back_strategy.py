# region imports
from AlgorithmImports import *
# endregion

class PullBackStrategy(QCAlgorithm):

    def initialize(self):
        self.set_start_date(2019, 1, 1)
        self.set_end_date(2024, 1, 1)
        self.set_cash(10000)
        self.spy=self.add_equity("SPY", Resolution.DAILY)
        self.sma200=self.sma(self.spy.symbol, 200, Resolution.DAILY)
        self.sma20=self.sma(self.spy.symbol,20, Resolution.DAILY)
        self.rsi=self.rsi(self.spy.symbol, 5, MovingAverageType.SIMPLE, Resolution.DAILY)
        self.SetWarmUp(200)

    def on_data(self, data: Slice):
        if not self.sma200.is_ready or not self.sma20.is_ready or not self.rsi.is_ready:
            return
        if self.spy.symbol in data:
            price=self.securities[self.spy.symbol].price
            if not self.portfolio.invested:
                if price>self.sma200.current.value and price<self.sma20.current.value and self.rsi.current.value<45:
                    self.set_holdings(self.spy.symbol,1)
                    self.log("BUY")
                    self.log(f"sma200:{self.sma200.current.value}")
                    self.log(f"sma20:{self.sma20.current.value}")
                    self.log(f"rsi:{self.rsi.current.value}")
                    self.log(f"Buy Price:{self.securities[self.spy.symbol].price}")
            if self.portfolio.invested:
                if price>self.sma20.current.value or self.rsi.current.value>65:
                    self.liquidate(self.spy.symbol)
                    self.log("SELL")
                    self.set_holdings(self.spy.symbol,1)
                    self.log(f"sma200:{self.sma200.current.value}")
                    self.log(f"sma20:{self.sma20.current.value}")
                    self.log(f"rsi:{self.rsi.current.value}")
                    self.log(f"Sell Price:{self.securities[self.spy.symbol].price}")
            

            
