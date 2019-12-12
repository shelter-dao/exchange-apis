from coinbase import CoinbasePipeline
from sma_golden_cross import SMAGoldenCross


import datetime as dt
import backtrader as bt
import backtrader.feeds as feeds
import backtrader.indicators as btind
import backtrader.analyzers as btanalyzers

if __name__ == '__main__':
    strategy = SMAGoldenCross
    startcash = 100000

    cerebro = bt.Cerebro(runonce=False, optreturn=False)

    cerebro.optstrategy(strategy, pfast=range(60,70), pslow=range(100,110) )

    one_year = dt.timedelta(days=365)
    days_100 = dt.timedelta(days=100)
    days_150 = dt.timedelta(days=150)
    days_30  = dt.timedelta(days=30)
    month_6  = dt.timedelta(days=180)
    start = dt.datetime.now() - one_year
    pipeline = CoinbasePipeline('BTC-USD',start=start, granularity=21600)
    dataframe = pipeline.get_data()

    data = feeds.PandasData(dataname=dataframe)
    cerebro.adddata(data)
    cerebro.broker.setcash(startcash)
    SharpeRatioDay = bt.analyzers.SharpeRatio
    cerebro.addanalyzer(SharpeRatioDay, _name='mysharpe',timeframe=bt.TimeFrame.Days)
    cerebro.addanalyzer(btanalyzers.AnnualReturn, _name='areturn')
    cerebro.addanalyzer(btanalyzers.DrawDown, _name='ddown')

    thestrats = cerebro.run()
