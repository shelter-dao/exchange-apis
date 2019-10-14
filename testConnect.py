import requests
import numpy as np
import pandas as pd

request = requests.get('https://api.bittrex.com/api/v1.1/public/getcurrencies')

# Convert request JSON into python dictionary
request_json = request.json()

# Convert python dictionary into a pandas DataFrame
currenciesFrame = pd.DataFrame(request_json['result'])
#print(currenciesFrame)

BtcEth = requests.get('https://api.bittrex.com/api/v1.1/public/getticker?market=BTC-ETH').json()
#print(BtcEth['result'])
print('Price of last trade:', BtcEth['result']['Last'], 'BTC/ETH')
