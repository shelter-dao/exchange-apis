from coinbase import CoinbasePipeline
from sma_golden_cross import SMAGoldenCross
from mean_reversion import MeanReversion

import datetime as dt
import backtrader as bt
import backtrader.feeds as feeds
import backtrader.indicators as btind
import backtrader.analyzers as btanalyzers

if __name__ == '__main__':
    strategy = MeanReversion
    startcash = 100000

    cerebro = bt.Cerebro(runonce=False, optreturn=False)

    cerebro.addstrategy(strategy)

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
    print('Starting Portfolio Value: %.2f' % cerebro.broker.getvalue())

    thestrats = cerebro.run()
    print(thestrats)

    print('\nFinal Portfolio Value: %.2f' % cerebro.broker.getvalue())
    print('\nSharpe Ratio:', thestrats[0].analyzers.mysharpe.get_analysis()['sharperatio'])
    print('\n2019 Annual Return:',(thestrats[0].analyzers.areturn.get_analysis()[2019] * 100), "%" )
    print('\nDraw Down:\n',
          '    Duration: %.2f' % thestrats[0].analyzers.ddown.get_analysis().get("len"),
          '    Percent: %.2f' % thestrats[0].analyzers.ddown.get_analysis().get("drawdown"), "%",
          '    Dollars: %.2f' % thestrats[0].analyzers.ddown.get_analysis().get("moneydown"))

    # cerebro.plot()

    # pipeline.change_graph()
    # pipeline.candlestick_graph()
