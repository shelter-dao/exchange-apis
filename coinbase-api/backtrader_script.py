from coinbase import CoinbasePipeline
import datetime as dt
import backtrader as bt
import backtrader.feeds as feeds

class PandasData(feeds.DataBase):
    params =(
        ('datetime', -1),
        ('open', -1),
        ('high', -1),
        ('low',-1),
        ('close', -1),
        ('volume', -1),
        ('openinterest', None),
    )

class TestStrategy(bt.Strategy):

    def log(self, txt, dt=None):
        ''' Logging function for this strategy'''
        dt = dt or self.datas[0].datetime.date(0)
        print('%s, %s' % (dt.isoformat(), txt))

    def __init__(self):
        # Keep a reference to the "close" line in the data[0] dataseries
        self.dataclose = self.datas[0].close

    def next(self):
        # Simply log the closing price of the series from the reference
        self.log('Close, %.2f' % self.dataclose[0])


cerebro = bt.Cerebro()

cerebro.addstrategy(TestStrategy)

one_year = dt.timedelta(days=365)
start = dt.datetime.now() - one_year
pipeline = CoinbasePipeline('BTC-USD',start=start)
dataframe = pipeline.get_data()
print('.', type(dataframe['datetime'][0]))


data = feeds.PandasData(dataname=dataframe)
print('data',data.datetime)
cerebro.adddata(data)
cerebro.broker.setcash(1000.00)

print('Starting Portfolio Value: %.2f' % cerebro.broker.getvalue())
cerebro.run()
print('Final Portfolio Value: %.2f' % cerebro.broker.getvalue())
