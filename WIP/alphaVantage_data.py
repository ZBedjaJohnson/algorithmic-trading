import os
import warnings
import requests
import pandas as pd
import backtrader
from pandas.io.json import json_normalize
API_KEY = os.environ.get('ALPHA_VANTAGE')

base_url = 'https://www.alphavantage.co/query?function='

def grab_Intraday_FX(curr1,curr2,interval,store=False):
    """
    Get exchange rate between curr1 and curr2

    OHLC data for past 24hrs

    Timeframe 1min, 5min, 15min, 30min, 60min

    Store (default false) - store returned dataframe as csv
    """
    
    req = requests.get('{}FX_INTRADAY&from_symbol={}&to_symbol={}&interval={}&outputsize=full&apikey={}'.format(base_url,curr1,curr2,interval,API_KEY))

    if req.status_code != 200:
        raise Exception('GET /intraday/ {}'.format(req.status_code))
    
    raw = req.json()

    # ohlc = pd.read_json(raw)

    print(raw['Time Series FX (1min)'].keys())

    # ohlc = pd.DataFrame(raw, columns=['date', 'open','high','low','close'])
    # print(ohlc.head())

    # if store == True:
    #     # ohlcv.to_pickle('./data/{}-{}-minute{}.pkl'.format(symbol,date,'-SANDBOX' if sandbox == True else ''))
    #     ohlcv.to_csv('./data/{}-{}-minute{}.csv'.format(symbol,date,'-SANDBOX' if sandbox == True else ''),index=False)
    # return ohlcv


grab_Intraday_FX('GBP','USD','1min')
