import requests        # for making http requests to binance
import json            # for parsing what binance sends back to us
import pandas as pd    # for storing and manipulating the data we get back
import numpy as np     # numerical python

import matplotlib.pyplot as plt # for charts and such

import datetime as dt  # for dealing with times

# Binance API url
root_url = root_url = 'https://api.binance.com/api/v1/klines'

# Function to get historical pricing data for specified symbol
def get_bars(symbol, interval = '1h'):
    url = root_url + '?symbol=' + symbol + '&interval=' + interval

    # Make an HTTP request to Binance API to grab json data and parse into Python
    # dictionary (!)
    data = json.loads(requests.get(url).text)

    # Make DataFrame
    df = pd.DataFrame(data)
    df.columns = ['open_time',
                  'o', 'h', 'l', 'c', 'v',
                  'close_time', 'qav', 'num_trades',
                  'taker_base_vol', 'taker_quote_vol', 'ignore']
                  # column names specified by API docs

    # Convert ms timestamps into Python datetime objects
    df.index = [dt.datetime.fromtimestamp(x/1000.0) for x in df.close_time]
    return df

# Get list of symbols where price is listed in ETH
symbols = json.loads(requests.get("https://api.binance.com/api/v1/exchangeInfo").text)
symbols = [symbol['symbol'] for symbol in symbols['symbols'] if symbol['quoteAsset'] == 'ETH']

# Download ETH pricing data in USD
ethusdt = get_bars('ETHUSDT')

price_data = []
new_symbols = []

# Download pricing data for each symbol listed in ETH, convert quote to USD
for symbol in symbols:
    print(symbol)
    data = get_bars(symbol)
    new_symbols.append(symbol.replace('ETH','USDT'))
    price_data.append(data['c'].astype('float') * ethusdt['c'].astype('float'))

# Plotting
combo = pd.concat(price_data, axis = 1)
combo.columns = new_symbols

combo.div(combo.ix[0]).plot(figsize=(16,9))

plt.show(block=True)
