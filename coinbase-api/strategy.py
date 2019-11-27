import datetime as dt
import backtrader as bt
import backtrader.indicators as btind

class TestStrategy(bt.Strategy):

    def log(self, txt, dt=None):
        ''' Logging function for this strategy'''
        dt = dt or self.datas[0].datetime.date(0)
        print('%s, %s' % (dt.isoformat(), txt))

    def __init__(self):
        # Keep a reference to the "close" line in the data[0] dataseries
        self.dataclose = self.datas[0].close
        self.sma = btind.SimpleMovingAverage(period=15)

        self.order = None
        self.hist_change = []

    def next(self):
        # Simply log the closing price of the series from the reference
        self.log('Close, %.5f' % self.dataclose[0])
        if self.sma > self.dataclose:
            self.order = self.buy(data=self.datas[0], size=1, exectype=None)
            print("BUY ORDER")
            pass
        elif   self.sma < self.dataclose:
            #do something here
            pass
