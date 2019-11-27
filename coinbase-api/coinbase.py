import cbpro as cbp
import datetime as dt
import pandas as pd
import time
import plotly.graph_objects as go

class CoinbasePipeline(object):
    def __init__(self, product_id, start, end=dt.datetime.now(), granularity=86400):
        self.product_id = product_id
        self.start = start
        self.end = end
        self.granularity = granularity

    def get_data(self):
        start = self.start
        end = self.end
        granularity = self.granularity
        product_id = self.product_id
        interval = 300 * granularity
        x = dt.timedelta(seconds=interval)
        temp_start = end - x
        hist_data = []

        while end.date() > start.date():
            pc = cbp.PublicClient()
            if temp_start < start:
                temp_start = start

            new_data = pc.get_product_historic_rates(product_id, start=temp_start, end=end, granularity=granularity)

            hist_data.extend(new_data)
            end = dt.datetime.fromtimestamp(new_data[-1][0])

            x = 300 * granularity
            delta = dt.timedelta(seconds=x)
            temp_start = end - delta
            pc.session.close()
            time.sleep(1)

        df = pd.DataFrame(hist_data)
        df.columns = ['datetime', 'low', 'high', 'open', 'close', 'volume']
        df.datetime = df.datetime.apply(lambda x: dt.datetime.fromtimestamp(x))
        df.set_index('datetime', inplace=True, drop=True)
        df = df.reindex(index=df.index[::-1])

        return df

    def candlestick_graph(self):
        df = self.get_data()
        fig = go.Figure(data=[go.Candlestick(x=df.index,
                        open=df['open'],
                        high=df['high'],
                        low=df['low'],
                        close=df['close'])])

        fig.show()
