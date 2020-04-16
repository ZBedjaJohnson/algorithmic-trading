import backtrader.feeds as btfeeds
import backtrader as bt

class IEXMinuteCSV(btfeeds.GenericCSVData):

  params = (
    ('nullvalue', float('NaN')),
 
    ('timeframe', bt.TimeFrame.Minutes),

    ('dtformat', ('%Y-%m-%d')),
    ('tmformat', ('%H:%M')),

    ('datetime', 0),
    ('time', 1),
    ('open', 2),
    ('high', 3),
    ('low', 4),
    ('close', 5),
    ('volume', 6),
    ('openinterest', -1)
)