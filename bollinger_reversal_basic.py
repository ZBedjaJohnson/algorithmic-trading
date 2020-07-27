import backtrader as bt
import backtrader.feeds as btfeeds
import backtrader.indicators as btind
import data_formats

class TestStrategy(bt.Strategy):
    def __init__(self):
        self.dataclose = self.datas[0].close

        self.bbands = btind.BollingerBands(period=20,devfactor=2)

        self.stoch = btind.Stochastic(period=14,period_dfast=3,period_dslow=3)

        self.orefs = list()

        self.short_signal = bt.And(self.dataclose > self.bbands.top, self.stoch.percK > 80)

        self.long_signal = bt.And(self.dataclose < self.bbands.bot, self.stoch.percK < 20)

    def notify_order(self, order):
        if order.status in [order.Submitted, order.Accepted]:
            return
        
        if order.status in [order.Completed]:
            if order.isbuy():
                self.log('BUY EXECUTED, Price: {}, Value: {}, Comm: {}'
                .format(order.executed.price,order.executed.value,order.executed.comm))
            elif order.issell():
                self.log('SELL EXECUTED, Price: {}, Value: {}, Comm: {}'
                .format(order.executed.price,order.executed.value,order.executed.comm))

            self.bar_executed = len(self)    

        elif order.status in [order.Canceled, order.Margin, order.Rejected]:
            self.log('Order Canceled/Margin/Rejected')

        self.orefs.remove(order.ref)


    def notify_trade(self, trade):
        if not trade.isclosed:
            return

        self.log('OPERATION PROFIT, GROSS {:.2f}, NET {:.2f}'.format(trade.pnl, trade.pnlcomm))
                    

    def log(self, txt):
        dt = self.data.datetime.datetime()
        print(dt, txt)


    def next(self):
        if self.orefs:
            return

        if not self.position:
            if self.long_signal[0] == True:
                self.log('BUY CREATE, {}'.format(self.dataclose[0]))
                mkt_buy = self.buy(size=100)
                self.orefs.append(mkt_buy.ref)

            elif self.short_signal[0] == True:
                self.log('SELL CREATE, {}'.format(self.dataclose[0]))
                mkt_sell = self.sell(size=100)
                self.orefs.append(mkt_sell.ref)
        else:
            if self.position.size > 0 and self.short_signal[0] == True:
                self.log('SELL CREATE, {}'.format(self.dataclose[0]))
                mkt_sell = self.sell(size=100)
                self.orefs.append(mkt_sell.ref)

            elif self.position.size < 0 and self.long_signal[0] == True:
                self.log('BUY CREATE, {}'.format(self.dataclose[0]))
                mkt_buy = self.buy(size=100)
                self.orefs.append(mkt_buy.ref)

def runstrat():
    cerebro = bt.Cerebro()

    datapath = ('./data/NET-202003-minute.csv')

    data = data_formats.IEXMinuteCSV(dataname=datapath)

    cerebro.adddata(data)
    
    cerebro.addstrategy(TestStrategy)

    cerebro.broker.setcash(10000)
    # cerebro.broker.setcommission(commission=0.0001)
    
    print('Starting Portfolio Value: {:.2f}'.format(cerebro.broker.getvalue()))

    cerebro.run()

    print('Final Portfolio Value: {:.2f}'.format(cerebro.broker.getvalue()))

    cerebro.plot()


if __name__ == '__main__':
    runstrat()