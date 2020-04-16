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
    Minuite OHLCV data for a specified day

    Date format - YYYYMMDD

    Sandbox (default false) - scrambled data for testing

    Store (default false) - store returned dataframe as csv

    50 credits per day
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


# grab_day_minute('AMD','20200408',True,True)

def grab_month_minute(symbol,date,store=False,sandbox=False):
    """
    Minuite OHLCV data for a specified month

    Date format - YYYYMM

    Sandbox (default false) - scrambled data for testing

    Store (default false) - store returned dataframe as csv

    50 credits per day (30 day month 1500 credits)
    """
    days_ohlcv = []
    for i in range(1,32):
        try:
            days_ohlcv.append(grab_day_minute('AMD','{}{:02d}'.format(date,i),False,sandbox))
        except:
            pass

    month_ohlcv = pd.concat(days_ohlcv)
    if store == True:
        month_ohlcv.to_csv('./data/{}-{}-minute{}.csv'.format(symbol,date,'-SANDBOX' if sandbox == True else ''),index=False)

    return month_ohlcv

grab_month_minute('AMD',202004,True)