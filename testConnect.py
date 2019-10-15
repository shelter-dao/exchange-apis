import requests
import numpy as np
import pandas as pd
import time
import json
import hmac
import hashlib
from urllib.parse import urljoin, urlencode
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from matplotlib import style
import threading


request = requests.get('https://api.bittrex.com/api/v1.1/public/getcurrencies')

# Convert request JSON into python dictionary
request_json = request.json()

# Convert python dictionary into a pandas DataFrame
currenciesFrame = pd.DataFrame(request_json['result'])
#print(currenciesFrame)

BtcEth = requests.get('https://api.bittrex.com/api/v1.1/public/getticker?market=BTC-ETH').json()
#print(BtcEth['result'])
print('Price of last trade on Bittrex:', BtcEth['result']['Last'], 'BTC/ETH')
BittrexPrice = float(BtcEth['result']['Last'])


# Get Binance last price
API_KEY = 'ludydX98VVtUImNCgLSHaikPrx3IWKGiev1KJ3XKz5VzaREKqPAbfEb9Jus9huuY'
SECRET_KEY = 'FzWhOlTP2uRVzyqfJGSGrNfrLnqbxZ6ekNVQ5clB8hXNb4HvZMW1rfsXUhMHLlsl'
BASE_URL = 'https://api.binance.com'

headers = {
    'X-MBX-APIKEY': API_KEY
}

class BinanceException(Exception):
    def __init__(self,status_code,data):
        self.status_code = status_code
        if data:
            self.code = data['code']
            self.msg = data['msg']
        else:
            self.code = None
            self.msg = None
        message = f"{status_code} [{self.code}] {self.msg}"

PATH = '/api/v1/time'
params = None

timestamp = int(time.time() * 1000)

url = urljoin(BASE_URL, PATH)
r = requests.get(url, params=params)
if r.status_code == 200:
    data = r.json()
    #print(f"diff={timestamp - data['serverTime']}ms")
else:
    raise BinanceException(status_code=r.status_code, data=r.json())

PATH = 'api/v3/ticker/price'
params = {
    'symbol': 'ETHBTC'
}

url = urljoin(BASE_URL, PATH)
r = requests.get(url, headers=headers, params=params)
BinancePrice = float(r.json()['price'])

if r.status_code == 200:
    print("Price of last trade on Binance:", BinancePrice, "BTC/ETH")
else:
    raise BinanceException(status_code=r.status_code, data=r.json())

if BinancePrice > BittrexPrice:
    difference = BinancePrice - BittrexPrice
    percent = difference / BittrexPrice * 100
    print("The price is ", percent, "percent higher on Binance")
else:
    difference = BittrexPrice - BinancePrice
    percent = difference / BinancePrice * 100
    print("The price is ", percent, "percent higher on Bittrex")

# Plot real time arbitrage opportunities between Binance and Bittrex

arbitrageData = pd.DataFrame(columns=['BinancePrice', 'BittrexPrice','% Difference'])

def addData():
    # Get current Time
    ts = time.localtime()
    current_time = time.strftime("%Y-%m-%d %H:%M:%S", ts)
    # Get Binance Price
    r = requests.get(url, headers=headers, params=params)
    BinancePrice = float(r.json()['price'])
    # Get Bittrex Price
    BtcEth = requests.get('https://api.bittrex.com/api/v1.1/public/getticker?market=BTC-ETH').json()
    BittrexPrice = float(BtcEth['result']['Last'])
    # Get percent difference
    difference = (BittrexPrice - BinancePrice) / BinancePrice * 100
    # Update Arbitrage Dataframe
    arbitrageData.loc[current_time] = [BinancePrice, BittrexPrice, difference]
    threading.Timer(3.0, addData).start()
    print(arbitrageData)


addData()





style.use('fivethirtyeight')

fig = plt.figure()
ax1 = fig.add_subplot(1, 1, 1)

# def animate(i):
#     graph_data =
