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

        # default to the maximum of 300 api calls
        interval = 300 * granularity
        delta = dt.timedelta(seconds=interval)
        #temp start is 300 bars back from defined end time
        temp_start = end - delta
        hist_data = []

        while end.date() > start.date():
            pc = cbp.PublicClient()
            # if defined timerange requires less than 300 calls, reset start time
            if temp_start < start:
                temp_start = start

            new_data = pc.get_product_historic_rates(product_id, start=temp_start, end=end, granularity=granularity)
            # append new data to historical data array
            hist_data.extend(new_data)
            # re-evaluate end to the earliest value in retreived data (300 bars back)
            end = dt.datetime.fromtimestamp(new_data[-1][0])
            interval = 300 * granularity
            delta = dt.timedelta(seconds=interval)
            # reset temp_start to be 300 bars back from new end value
            temp_start = end - delta
            pc.session.close()
            time.sleep(1)

        df = pd.DataFrame(hist_data)
        df.columns = ['datetime', 'low', 'high', 'open', 'close', 'volume']
        df.datetime = df.datetime.apply(lambda x: dt.datetime.fromtimestamp(x))
        df['change'] = df.apply(lambda row: ((row['close'] - row['open'])/row['open'] * 100), axis=1 )
        df.set_index('datetime', inplace=True, drop=True)
        df = df.iloc[::-1]
        return df

    def candlestick_graph(self, df=None):
        df = df or self.get_data()
        fig = go.Figure(data=[go.Candlestick(x=df.index,
                        open=df['open'],
                        high=df['high'],
                        low=df['low'],
                        close=df['close'])])

        fig.show()
    def change_graph(self, df=None):
        df = df or self.get_data()
        fig = go.Figure(data=go.Scatter(x=df.index, y=df.change))
        fig.show()
