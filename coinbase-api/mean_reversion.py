import datetime as dt
import backtrader as bt
import backtrader.indicators as btind

class MeanReversion(btind.SignalStrategy):
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
        ("devfactor", 2)
        # ("size", 20)
    )

    def log(self, txt, dt=None):
        dt = dt or self.datas[0].datetime.date(0)
        print('%s, %s' % (dt.isoformat(), txt))

    def __init__():
        # Reference to "close" line
        self.dataclose = self.datas[0].close

        # Bollinger Band indicator
        self.boll = btind.BollingerBands(period=self.p.period, devfactor=self.p.devfactor)
        # self.sx = bt.indicators.CrossDown(self.data.close, self.boll.lines.top)
        # self.lx = bt.indicators.CrossUp(self.data.close, self.boll.lines.bot)

    def next():
        # Log closing
        self.log('Close, %.2f' % self.dataclose)

        if self.order:
            return
        # if we hold no current position
        if not self.position:
            if self.dataclose < self.boll.lines.bot:
                # execute buy with stop order price set to top bollinger band
                self.buy(exectype=bt.Order.Stop, price=self.boll.lines.bot[0])
        else:
            # if our position is a buy, place a sell limit order at the bollinger band mid line
            if self.position.size > 0:
                self.sell(exectype=bt.Order.Limit, price=self.boll.lines.mid[0], size=self.p.size)
