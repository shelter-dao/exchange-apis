from coinbase import CoinbasePipeline
from strategy import TestStrategy

import datetime as dt
import backtrader as bt
import backtrader.feeds as feeds
import backtrader.indicators as btind
import backtrader.analyzers as btanalyzers

strategy = TestStrategy

cerebro = bt.Cerebro()

cerebro.addstrategy(strategy)

one_year = dt.timedelta(days=365)
start = dt.datetime.now() - one_year*2
pipeline = CoinbasePipeline('BTC-USD',start=start)
dataframe = pipeline.get_data()


data = feeds.PandasData(dataname=dataframe)
print('data',data)
cerebro.adddata(data)
cerebro.broker.setcash(10000.00)
cerebro.addanalyzer(btanalyzers.SharpeRatio, _name='mysharpe')
cerebro.addanalyzer(btanalyzers.AnnualReturn, _name='areturn')
cerebro.addanalyzer(btanalyzers.DrawDown, _name='ddown')

print('Starting Portfolio Value: %.2f' % cerebro.broker.getvalue())
thestrats = cerebro.run()
print('\nFinal Portfolio Value: %.2f' % cerebro.broker.getvalue())
print('\nSharpe Ratio:', thestrats[0].analyzers.mysharpe.get_analysis()['sharperatio'] )
print('\n2018 Annual Return:',(thestrats[0].analyzers.areturn.get_analysis()[2018] * 100), '%' )
print('\nDraw Down:\n',
      '    Durration: ',thestrats[0].analyzers.ddown.get_analysis().get("len"),
      '    Percent: %.2f' % thestrats[0].analyzers.ddown.get_analysis().get("drawdown"), "%",
      '    Dollars: %.2f' % thestrats[0].analyzers.ddown.get_analysis().get("moneydown"))
