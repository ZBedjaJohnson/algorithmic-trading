# Algorithmic Trading

## Setup
### Conda
Setup environment using the following commands:

```bash
conda env create -f environment.yml

conda activate backtrader
```

### API Keys
Pricing data for stocks is pulled from IEX Cloud, an API key can be acquired free [here](https://iexcloud.io/). A sandbox and a live key will be provided. During data pulling development, the sandbox key can be used, however, the data received will be scrambled, hence unsuitable for backtesting. 

FX pricing is pulled from Alpha Vantage, a free API key can be acquired [here](https://www.alphavantage.co/support/#api-key).

To set the API keys as environmental variables, use the following command:

```bash
conda env config vars set var=value
```

Where var and value are for the corrosponding API keys:
-   IEX Cloud = 'IEX_SECRET'
-   IEX Cloud Sandbox = 'IEX_SANDBOX'
-   Alpha Vantage = 'ALPHA_VANTAGE'

Once setting the keys, activate the env once again.

```bash
conda activate backtrader
```

Then to confirm the keys have been set correctly, use the following command.

```bash
conda env config vars list
```

## Pulling Data

Data for a majority of US Stocks and ETFs alongside some international symbols can be pulled using iex_data.py

The functions _pull_day_minute_ and _pull_month_minute_ can be used to pull a single day or month worth of intraday data on a 1-minute timescale.

Instructions for each function are provided with docstrings. The data is returned by the function as a dataframe by default, however, using __store=True_ will output a CSV file in the _/data_ folder (useful especially with monthly data).

_Warning - sandbox=True should only be used for debugging data pulling, the pricing produced is scrambled and completely useless for backtesting._

### Example 1
Intraday data for ticker __NET__ for the month of March 2020. The true arg will create a CSV file with path: _data/NET-202003-minute.csv_

```python
pull_month_minute('NET',202003,True)
```
### Example 2
Intraday data for ticker __TSLA__ for 12th March 2020. Store will default to false and the function will return a dataframe.

```python
data = pull_day_minute('TSLA',20200312)
```

## Trend Reversal Algorithm



