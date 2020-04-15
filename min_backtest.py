import backtrader as bt
import backtrader.feeds as btfeeds
import data_formats

class TestStrategy(bt.Strategy):
    def __init__(self):
        self.dataclose = self.datas[0].close

        self.order = None


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

        self.order = None


    def notify_trade(self, trade):
        if not trade.isclosed:
            return

        self.log('OPERATION PROFIT, GROSS {}, NET {}'.format(trade.pnl, trade.pnlcomm))
                    


    def log(self, txt):
        dt = self.data.datetime.datetime()
        print(dt, txt)


    def next(self):
        if self.order:
            return

        if not self.position:
            if self.dataclose[0] < self.dataclose[-1]:
                if self.dataclose[-1] < self.dataclose[-2]:
                    self.log('BUY CREATE, {}'.format(self.dataclose[0]))
                    self.order = self.buy()

        else:
            if len(self) > self.bar_executed + 1:
                if self.dataclose[0] > self.dataclose[-1]:
                    if self.dataclose[-1] > self.dataclose[-2]:
                        self.log('SELL CREATE, {}'.format(self.dataclose[0]))
                        self.order = self.sell()

def runstrat():
    cerebro = bt.Cerebro()

    datapath = ('./data/AMD-202003-minute.csv')

    data = data_formats.IEXMinuteCSV(dataname=datapath)

    cerebro.adddata(data)
    
    cerebro.addstrategy(TestStrategy)

    cerebro.broker.setcash(1000)
    # cerebro.broker.setcommission(commission=0,margin=1)
    
    print('Starting Portfolio Value: {}'.format(cerebro.broker.getvalue()))

    cerebro.run()

    print('Final Portfolio Value: {}'.format(cerebro.broker.getvalue()))

    cerebro.plot()


if __name__ == '__main__':
    runstrat()