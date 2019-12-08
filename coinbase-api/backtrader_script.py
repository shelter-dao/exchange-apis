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

    cerebro.optstrategy(strategy, pfast=range(1,20), )


    one_year = dt.timedelta(days=365)
    days_100 = dt.timedelta(days=100)
    days_150 = dt.timedelta(days=150)
    days_30  = dt.timedelta(days=30)
    month_6  = dt.timedelta(days=180)
    start = dt.datetime.now() - days_30
    pipeline = CoinbasePipeline('BTC-USD',start=start, granularity=3600)
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
    print('\nSharpe Ratio:', thestrats[0])
    # print('\n2019 Annual Return:',(thestrats[0].analyzers.areturn.get_analysis()[2019] * 100), "%" )
    # print('\nDraw Down:\n',
    #       '    Durration: %.2f' % thestrats[0].analyzers.ddown.get_analysis().get("len"),
    #       '    Percent: %.2f' % thestrats[0].analyzers.ddown.get_analysis().get("drawdown"), "%",
    #       '    Dollars: %.2f' % thestrats[0].analyzers.ddown.get_analysis().get("moneydown"))

    # cerebro.plot()

    # pipeline.change_graph()
    # pipeline.candlestick_graph()
#pfast=range(10,30), pslow=range(40-70)
