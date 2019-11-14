import cbpro
import datetime as dt
import numpy as np
import pandas as pd
import time
import requests

# initialize coinbase pro client with public functions
product_id = 'BTC-USD'

# set end to current time and iterate backwards to specified start
start = dt.datetime(2019, 8, 1)
end = dt.datetime.now()
print(type(end))

hist_data = []

# while end != start:
for x in [1,2,3]:
    pc = cbpro.PublicClient()
    print(end)
    param_end = end.ToString('yyyy-mm-dd')
    print(param_end)
    new_data = pc.get_product_historic_rates(product_id, end=param_end, granularity=86400)
    hist_data.extend(new_data)
    end = dt.datetime.fromtimestamp(new_data[-1][0])
    print(end)
    print('')
    print(pc.session)
    time.sleep(5)
