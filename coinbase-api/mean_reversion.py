import datetime as dt
import backtrader as bt
import backtrader.indicators as btind

class MeanReversion(bt.SignalStrategy):
    '''
    A mean-reversion strategy bollinger band strategy
    Entry Signal:
      - Long:
          - Price closes below lower band
          - Stop Order
    Exit Signal:
      - Long:
          - Price touches median line
    '''

    params = (
        ("period", 20),
        ("devfactor", 2),
        ("size", 20)
    )

    def log(self, txt, dt=None):
        dt = dt or self.datas[0].datetime.date(0)
        print('%s, %s' % (dt.isoformat(), txt))

    def __init__(self):
        # Reference to "close" line
        self.close = self.data.close
        self.order = None
        # Bollinger Band indicator
        self.boll = btind.BollingerBands(period=self.p.period, devfactor=self.p.devfactor)
        # self.sx = bt.indicators.CrossDown(self.data.close, self.boll.lines.top)
        # self.lx = bt.indicators.CrossUp(self.data.close, self.boll.lines.bot)

    def next(self):
        # Log closing price

        if self.order:
            self.log('Current Order, %', self.order)
            return
        else:
            if not self.position:   # no position
                if self.close < self.boll.lines.bot:
                    # execute buy with stop order price set to  bollinger band
                    self.buy(exectype=bt.Order.Stop, price=self.boll.lines.bot[0])
                    self.log('BUY CREATE, %.2f' % self.close[0])
            else:   # have position
                # if our position is a buy, place a sell limit order at the bollinger band mid line
                if self.position.size > 0:
                    self.log('SELL CREATE, %.2f' % self.close[0])
                    self.sell(exectype=bt.Order.Limit, price=self.boll.lines.mid[0])
