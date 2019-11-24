import cbpro as cbp
import datetime as dt
import numpy as np
import pandas as pd
import time
import plotly.graph_objects as go
import requests

class DataAPI(object):
    def __init__(self, product_id, start, end=dt.datetime.now(), granularity='86400'):
        self.product_id = product_id
        self.start = start
        self.end = end
        self.granularity = granularity

    def get_data(self):
        start = self.start
        end = self.end
        granularity = self.granularity
        product_id = self.product_id

        temp_start = end - dt.timedelta(seconds=300*granularity)
        hist_data = []

        while end > start:
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

        df = DataFrame(hist_data)
        df.columns = ['datetime', 'low', 'high', 'open', 'close', 'volume']
        df.time = df.time.apply(lambda x: dt.datetime.fromtimestamp(x))
        return df

one_year = dt.timedelta(days=365)
start = dt.datetime.now() - one_year
pipeline = DataAPI(product_id='BTC-USD', start=start)
data = pipeline.get_data()

print(data.iloc[:5])
print('---')
print(data['time'].iloc[-1])
print(data['time'].iloc[0])

# # initialize coinbase pro client with public functions
# product_id = 'BTC-USD'
#
# # set end to current time and iterate backwards to specified start
# start = dt.datetime(2017, 9, 1)
# end = dt.datetime(2019, 9, 1)
# granularity = 86400
# temp_start = end - dt.timedelta(seconds=300*granularity)
#
# hist_data = []
#
# while end > start:
#     pc = cbp.PublicClient()
#
#     if temp_start < start:
#         temp_start = start
#
#     new_data = pc.get_product_historic_rates(product_id, start=temp_start, end=end, granularity=granularity)
#
#     hist_data.extend(new_data)
#
#     end = dt.datetime.fromtimestamp(new_data[-1][0])
#     temp_start = end - dt.timedelta(seconds=300*granularity)
#
#     print(end)
#     print(len(new_data))
#     print(len(hist_data))
#     print('')
#     pc.session.close()
#     time.sleep(1)
#
# df = pd.DataFrame(hist_data)
# df.columns = ['datetime', 'low', 'high', 'open', 'close', 'volume']
# df.time = df.time.apply(lambda x: dt.datetime.fromtimestamp(x))
# print(df.iloc[:5])
# print('---')
# print(df['time'].iloc[-1])
# print(df['time'].iloc[0])


# # Candlestick Graph
# fig = go.Figure(data=[go.Candlestick(x=df['time'],
#                 open=df['open'],
#                 high=df['high'],
#                 low=df['low'],
#                 close=df['close'])])
#
# fig.show()
