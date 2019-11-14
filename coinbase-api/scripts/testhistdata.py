import cbpro as cbp
import datetime as dt
import numpy as np
import pandas as pd
import time
import requests

# initialize coinbase pro client with public functions
product_id = 'BTC-USD'

# set end to current time and iterate backwards to specified start
start = dt.datetime(2017, 9, 1)
end = dt.datetime(2019, 9, 1)
granularity = 86400
temp_start = end - dt.timedelta(seconds=300*granularity)

hist_data = []

while end > start:
    pc = cbp.PublicClient()

    if temp_start < start:
        temp_start = start

    new_data = pc.get_product_historic_rates(product_id, start=temp_start, end=end, granularity=granularity)

    hist_data.extend(new_data)

    end = dt.datetime.fromtimestamp(new_data[-1][0])
    temp_start = end - dt.timedelta(seconds=300*granularity)

    print(end)
    print(len(new_data))
    print(len(hist_data))
    print('')
    pc.session.close()
    time.sleep(1)

print(hist_data[0:5])
print('---')
print(dt.datetime.fromtimestamp(hist_data[-1][0]))
print(dt.datetime.fromtimestamp(hist_data[0][0]))
