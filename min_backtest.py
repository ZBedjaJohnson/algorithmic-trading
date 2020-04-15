import backtrader as bt
import backtrader.feeds as btfeeds
import data_formats

class TestStrategy(bt.Strategy):

    def log(self, txt):
        dt = self.data.datetime.time()

        print(dt, txt)
        # dt = dt or self.datas[0].time
        # print('%s, %s' % (dt.isoformat(), txt))



    def __init__(self):
        # Keep a reference to the "close" line in the data[0] dataseries
        self.dataclose = self.datas[0].close

    def next(self):
        # Simply log the closing price of the series from the reference
        self.log('Close, %.2f' % self.dataclose[0])


def runstrat():
    cerebro = bt.Cerebro(stdstats=False)

    cerebro.addstrategy(bt.Strategy)

    datapath = ('./data/TSLA-20200414-minute.csv')

    data = data_formats.IEXMinuteCSV(dataname=datapath)

    cerebro.addstrategy(TestStrategy)
    
    cerebro.adddata(data)

    cerebro.broker.setcash(100000.0)

    print('Starting Portfolio Value: {}'.format(cerebro.broker.getvalue()))

    cerebro.run()

    print('Final Portfolio Value: {}'.format(cerebro.broker.getvalue()))

    cerebro.plot(style='candle')


if __name__ == '__main__':
    runstrat()