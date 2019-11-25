from coinbase import CoinbasePipeline
import datetime as dt
import backtrader as bt
import backtrader.feeds as feeds
import backtrader.indicators as btind
import backtrader.analyzers as btanalyzers

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

        self.order = None

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




cerebro = bt.Cerebro()

cerebro.addstrategy(TestStrategy)

one_year = dt.timedelta(days=365)
start = dt.datetime.now() - one_year*3
pipeline = CoinbasePipeline('BTC-USD',start=start)
dataframe = pipeline.get_data()
print(dataframe)
# print('.', dataframe['datetime'][0])


data = feeds.PandasData(dataname=dataframe)
print('data',data)
cerebro.adddata(data)
cerebro.broker.setcash(10000.00)
cerebro.addanalyzer(btanalyzers.SharpeRatio, _name='mysharpe')
cerebro.addanalyzer(btanalyzers.AnnualReturn, _name='areturn')
cerebro.addanalyzer(btanalyzers.DrawDown, _name='ddown')

print('Starting Portfolio Value: %.2f' % cerebro.broker.getvalue())
thestrats = cerebro.run()
print('Final Portfolio Value: %.2f' % cerebro.broker.getvalue())
print('Sharpe Ratio:', thestrats[0].analyzers.mysharpe.get_analysis()['sharperatio'] )
print('Annual Return:',thestrats[0].analyzers.areturn.get_analysis() )
print('Draw Down:',thestrats[0].analyzers.ddown.get_analysis() )
