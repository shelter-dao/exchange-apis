import cbpro
import datetime as dt
import numpy as np
import pandas as pd
import time

# initialize coinbase pro client with public functions
pc = cbpro.PublicClient()
product_id = 'BTC-USD'

# set end to current time and iterate backwards to specified start
start = dt.datetime(2019, 8, 1)
end = dt.datetime.now()

hist_data = []

# while end != start:
for x in [1,2,3]:
    print(end)
    new_end = end
    print(new_end)
    new_data = pc.get_product_historic_rates(product_id, end=new_end, granularity=86400)
    hist_data.extend(new_data)
    end = dt.datetime.fromtimestamp(new_data[-1][0])
    print(end)
    print('')
    time.sleep(5)
