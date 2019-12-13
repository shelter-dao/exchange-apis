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
        ("devfactor", 1),
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

    def notify_order(self, order):

        if order.status in [order.Submitted, order.Accepted]:
            # Buy/Sell order submitted/accepted to/by broker - Nothing to do
            return

        # Check if an order has been completed
        # Attention: broker could reject order if not enough cash
        if order.status in [order.Completed]:
            if order.isbuy():
                self.log(
                    'BUY EXECUTED, Price: %.2f, Cost: %.2f, Position: %.2f' %
                    (order.executed.price,
                     order.executed.value,
                     self.position.size))

                self.buyprice = order.executed.price
                self.buycomm = order.executed.comm
            else:  # Sell
                 self.log('SELL EXECUTED, Price: %.2f, Cost: %.2f, Position: %.2f' %
                         (order.executed.price,
                          order.executed.value,
                          self.position.size))

            self.bar_executed = len(self)

        elif order.status in [order.Canceled, order.Margin, order.Rejected]:
            self.log('Order Canceled/Margin/Rejected')

        self.order = None

    def notify_trade(self,trade):
        if not trade.isclosed:
            return
        else:
            self.log('OPERATION PROFIT, GROSS {0:8.2f}, NET {1:8.2f}'.format(
                trade.pnl, trade.pnlcomm))

    def next(self):
        # Log closing price
        print(self.order)
        if self.order:
            self.log('Current Order, %', self.order)
            print("here")
            return

        else:
            if self.position.size == 0:   # no position
                if self.close < self.boll.lines.bot:
                    # execute buy with stop order price set to  bollinger band
                    self.order = self.buy(exectype=bt.Order.Stop, price=self.boll.lines.bot[0])
                    self.log('BUY CREATE, %.2f' % self.close[0])
            else:   # have position
                # if our position is a buy, place a sell limit order at the bollinger band mid line
                if self.position.size > 0:
                    print(self.position.size)
                    self.log('SELL CREATE, %.2f' % self.close[0])
                    self.order = self.sell(exectype=bt.Order.Limit, price=self.boll.lines.mid[0])
