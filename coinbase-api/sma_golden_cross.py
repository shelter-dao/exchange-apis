import datetime as dt
import backtrader as bt
import backtrader.indicators as btind

class SMAGoldenCross(bt.SignalStrategy):
    params = (('pfast', 32), ('pslow', 170),)

    def log(self, txt, dt=None):
        ''' Logging function for this strategy'''
        dt = dt or self.datas[0].datetime.date(0)
        print('%s, %s' % (dt.isoformat(), txt))

    def __init__(self):
        # 12 hour sma
        self.sma_12hr = btind.SimpleMovingAverage(period=self.p.pfast)
        # 30 day sma
        self.sma_30day = btind.SimpleMovingAverage(period=self.p.pslow)
        self.gsma = btind.CrossOver(self.sma_12hr, self.sma_30day)
        # used to determine if order has executed
        self.order = None
        # self.signal_add(bt.SIGNAL_LONG, bt.ind.CrossOver(sma_12hr, sma_30day))

        self.dataclose = self.datas[0].close

    def notify_order(self, order):

        if order.status in [order.Submitted, order.Accepted]:
            # Buy/Sell order submitted/accepted to/by broker - Nothing to do
            return

        # Check if an order has been completed
        # Attention: broker could reject order if not enough cash
        if order.status in [order.Completed]:
            if order.isbuy():
                # self.log(
                #     'BUY EXECUTED, Price: %.2f, Cost: %.2f, Position: %.2f' %
                #     (order.executed.price,
                #      order.executed.value,
                #      self.position.size))

                self.buyprice = order.executed.price
                self.buycomm = order.executed.comm
            # else:  # Sell
            #      self.log('SELL EXECUTED, Price: %.2f, Cost: %.2f, Position: %.2f' %
            #              (order.executed.price,
            #               order.executed.value,
            #               self.position.size))

            self.bar_executed = len(self)

        # elif order.status in [order.Canceled, order.Margin, order.Rejected]:
            # self.log('Order Canceled/Margin/Rejected')


    def next(self):
        if self.gsma > 0:
            # print("Positive CrossOverf" )
            # self.log('BUY CREATE, %.2f' % self.dataclose[0])
            self.order = self.buy()
        # if current bar is 7% higher than executed bar, SELL
        else:
            if self.position.size > 0:
                sell_percent = 1.05
                sell_price = sell_percent * self.order.executed.price
                # difference = self.bar_executed - len(self)
                if self.dataclose[0] >= sell_price:
                    # self.log('High SELL CREATE, %.2f' % self.dataclose[0])
                    # self.log('Current position size:, %.2f' % self.position.size)
                    # print(self.dataclose[0])
                    self.order = self.sell()

    def stop(self):
        pnl = round(self.broker.getvalue() - 100000,2)
        print('pfast: {} pslow: {} Final PnL: {}'.format(
            self.params.pfast, self.params.pslow, pnl))
