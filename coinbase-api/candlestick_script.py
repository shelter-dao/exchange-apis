import datetime as dt

from coinbase import CoinbasePipeline

one_year = dt.timedelta(days=365)
start = dt.datetime.now() - one_year*2

pipeline = CoinbasePipeline('BTC-USD',start=start)

pipeline.candlestick_graph()
