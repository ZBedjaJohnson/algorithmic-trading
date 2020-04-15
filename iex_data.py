import os
import warnings
import requests
import pandas as pd
import backtrader

IEX_API = os.environ.get('IEX_SECRET')
IEX_SANDBOX = os.environ.get('IEX_SANDBOX')

base_url = 'https://cloud.iexapis.com/stable/'
sandbox_url = 'https://sandbox.iexapis.com/stable/'

def grab_day_minute(symbol,date,store=False,sandbox=False):
    """
    Minuite OHLCV data for a specified date

    Date format - YYYYMMDD

    Sandbox (default false) - scrambled data for testing

    Store (default false) - store returned dataframe
    """
    if sandbox == True:
        warnings.warn('SANDBOX DATA')
        req = requests.get('{}/stock/{}/chart/date/{}?token={}'.format(sandbox_url,symbol,date,IEX_SANDBOX))
    else:
        req = requests.get('{}/stock/{}/chart/date/{}?token={}'.format(base_url,symbol,date,IEX_API))

    if req.status_code != 200:
        raise Exception('GET /intraday/ {}'.format(req.status_code))
    
    raw = req.json()

    ohlcv = pd.DataFrame(raw, columns=['date','minute', 'marketOpen','marketHigh','marketLow','marketClose','marketVolume'])
    
    if store == True:
        # ohlcv.to_pickle('./data/{}-{}-minute{}.pkl'.format(symbol,date,'-SANDBOX' if sandbox == True else ''))
        ohlcv.to_csv('./data/{}-{}-minute{}.csv'.format(symbol,date,'-SANDBOX' if sandbox == True else ''),index=False)
    return ohlcv


grab_day_minute('TSLA','20200415',True)
