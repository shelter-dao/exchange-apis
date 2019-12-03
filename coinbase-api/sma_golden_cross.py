import datetime as dt
import backtrader as bt
import backtrader.indicators as btind

class SMAGoldenCross(bt.SignalStrategy):

    params = (('pfast', 12), ('pslow',240),)
    # def log(self, txt, dt=None):
    #     ''' Logging function for this strategy'''
    #     dt = dt or self.datas[0].datetime.date(0)
    #     print('%s, %s' % (dt.isoformat(), txt))

        # Notify when signal is triggered
        # Provide the price of order placed
        # Notify when order completed
        # Notify when Stop-loss executed

    def __init__(self):
        # 12 hour sma
        sma_12hr = btind.SimpleMovingAverage(period=self.p.pfast)
        # 30 day sma
        sma_30day = btind.SimpleMovingAverage(period=self.p.pslow)
        # used to determine if order has executed
        self.order = None
        # self.signal_add(bt.SIGNAL_LONG, bt.ind.CrossOver(sma_12hr, sma_30day))
        print(bt.ind.CrossOver(sma_12hr,sma_30day))
