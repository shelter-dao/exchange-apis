from coinbase import CoinbasePipeline
import datetime as dt
import backtrader as bt
import backtrader.feeds as feeds
import backtrader.indicators as btind

# class PandasData(feed.DataBase):
#     params =(
#         ('nocase', True),
#         ('datetime', 0),
#         ('open', -1),
#         ('high', -1),
#         ('low',-1),
#         ('close', -1),
#         ('volume', -1),
#         ('openinterest', None),
#     )
#     print('classdefined')

class TestStrategy(bt.Strategy):

    def log(self, txt, dt=None):
        ''' Logging function for this strategy'''
        dt = dt or self.datas[0].datetime.date(0)
        print('%s, %s' % (dt.isoformat(), txt))

    def __init__(self):
        # Keep a reference to the "close" line in the data[0] dataseries
        self.dataclose = self.datas[0].close
        self.sma = btind.SimpleMovingAverage(period=15)

    def next(self):
        # Simply log the closing price of the series from the reference
        self.log('Close, %.5f' % self.dataclose[0])
        if self.sma > self.dataclose:
            #do somethign
            pass
        elif   self.sma < self.dataclose:
            #do something here
            pass
        



cerebro = bt.Cerebro()

cerebro.addstrategy(TestStrategy)

one_year = dt.timedelta(days=365)
start = dt.datetime.now() - one_year
pipeline = CoinbasePipeline('ETH-BTC',start=start)
dataframe = pipeline.get_data()
print(dataframe)
# print('.', dataframe['datetime'][0])


data = feeds.PandasData(dataname=dataframe)
print('data',data)
cerebro.adddata(data)
cerebro.broker.setcash(10000.00)

print('Starting Portfolio Value: %.2f' % cerebro.broker.getvalue())
cerebro.run()
print('Final Portfolio Value: %.2f' % cerebro.broker.getvalue())
