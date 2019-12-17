from coinbase import CoinbasePipeline
from mean_reversion import MeanReversion

import numpy as np
import datetime as dt
import pandas as pd
import backtrader as bt
import backtrader.feeds as feeds
import backtrader.indicators as btind
import backtrader.analyzers as btanalyzers

if __name__ == '__main__':
    strategy = MeanReversion
    startcash = 10 #BTC

    cerebro = bt.Cerebro(runonce=False, optreturn=False)
    cerebro.optstrategy(strategy, period=range(1,40),
                                  devfactor=range(1,40))

    # one_year = dt.timedelta(days=365)
    # days_100 = dt.timedelta(days=100)
    # days_150 = dt.timedelta(days=150)
    # days_30  = dt.timedelta(days=30)
    # month_6  = dt.timedelta(days=180)
    # start = dt.datetime.now() - days_100
    # pipeline = CoinbasePipeline('BTC-USD',start=start, granularity=3600)
    # dataframe = pipeline.get_data()

    dataframe = pd.read_csv("./hist-data/ETH-BTC-100d-1hr-12-16.csv",
                            index_col="datetime",
                            parse_dates=['datetime'])

    data = feeds.PandasData(dataname=dataframe)
    cerebro.adddata(data)
    cerebro.broker.setcash(startcash)
    cerebro.broker.setcommission(commission=0.005)
    SharpeRatioDay = bt.analyzers.SharpeRatio
    cerebro.addanalyzer(SharpeRatioDay, _name='mysharpe',timeframe=bt.TimeFrame.Days)
    cerebro.addanalyzer(btanalyzers.AnnualReturn, _name='areturn')
    cerebro.addanalyzer(btanalyzers.DrawDown, _name='ddown')

    opt_runs= cerebro.run()

    # Generate results list
    final_results_list = []
    for run in opt_runs:
        for strategy in run:
            value = strategy.value
            PnL = round(value - startcash,5)
            period = strategy.params.period
            devfactor = strategy.params.devfactor
            final_results_list.append([period,PnL,devfactor])
    #Sort Results List
    by_period = sorted(final_results_list, key=lambda x: x[0])
    by_PnL = sorted(final_results_list, key=lambda x: x[1], reverse=True)
    by_devfactor = sorted(final_results_list, key=lambda x: x[2])
    print(by_PnL[:10])

    #Print results
    # print('Results: Ordered by period:')
    # for result in by_period:
    #     print('Period: {}, Devfactor: {}, PnL: {}'.format(result[0], result[2], result[1]))
    # print('Results: Ordered by Profit:')
    # for result in by_PnL:
    #     # print('Period: {}, Devfactor: {}, PnL: {}'.format(result[0], result[2], result[1]))
    # print('Results: Ordered by Profit:')
    # for result in by_devfactor:
    #     print('Period: {}, Devfactor: {}, PnL: {}'.format(result[0], result[2], result[1]))
