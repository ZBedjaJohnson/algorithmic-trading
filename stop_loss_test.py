import backtrader as bt
import backtrader.feeds as btfeeds
import backtrader.indicators as btind
import data_formats

class TestStrategy(bt.Strategy):
    def __init__(self):
        self.dataclose = self.datas[0].close

        self.orefs = list()

        self.loss_perc = 0.0025
        self.risk_perc = 0.05

    def notify_order(self, order):
        if order.status in [order.Submitted, order.Accepted]:
            return
        
        if order.status in [order.Completed]:
            if order.isbuy():
                self.log('BUY EXECUTED, Price: {}, Value: {}, Comm: {}, Type: {}'
                .format(order.executed.price,order.executed.value,order.executed.comm,order.exectype))
            elif order.issell():
                self.log('SELL EXECUTED, Price: {}, Value: {}, Comm: {}, Type: {}'
                .format(order.executed.price,order.executed.value,order.executed.comm,order.exectype))

            self.bar_executed = len(self)    

        elif order.status in [order.Canceled, order.Margin, order.Rejected]:
            self.log('Order Canceled/Margin/Rejected')

        self.orefs.remove(order.ref)


    def notify_trade(self, trade):
        if not trade.isclosed:
            return

        self.log('OPERATION PROFIT, GROSS {:.2f}, NET {:.2f}, CASH: {:.2f}'.format(trade.pnl, trade.pnlcomm, self.broker.get_cash()))
                    

    def log(self, txt):
        dt = self.data.datetime.datetime()
        print(dt, txt)


    def next(self):
        if self.orefs:
            return

        if not self.position:
            if self.dataclose[0] > self.dataclose[-1]:
                if self.dataclose[-1] > self.dataclose[-2]:
                    self.log('BUY CREATE, Price: {}, QTY: {}'.format(self.dataclose[0],self.pos_size()))
                    mkt_buy = self.buy(size=self.pos_size(), exectype=bt.Order.Market, transmit=False)
                    stp_sell = self.sell(price=self.stop_price(mkt_buy.isbuy()),size=mkt_buy.size, exectype=bt.Order.Stop, transmit=True,parent=mkt_buy)
                    self.orefs.extend([mkt_buy.ref,stp_sell.ref])


    def pos_size(self):
        
        size = (self.broker.get_cash() * self.risk_perc) / (self.dataclose[0] * self.loss_perc)

        return round(size,0)


    def stop_price(self,dir):
        if dir == True:
            stoploss = self.dataclose[0] - self.dataclose[0] * self.loss_perc
        else:
            stoploss = self.dataclose[0] + self.dataclose[0] * self.loss_perc

        return round(stoploss,2)


def runstrat():
    cerebro = bt.Cerebro()

    datapath = ('./data/AMD-202002-minute.csv')

    data = data_formats.IEXMinuteCSV(dataname=datapath)

    cerebro.adddata(data)
    
    cerebro.addstrategy(TestStrategy)

    cerebro.broker.setcash(10000)
    cerebro.broker.setcommission(commission=0,leverage=20)
    
    print('Starting Portfolio Value: {:.2f}'.format(cerebro.broker.getvalue()))

    cerebro.run()

    print('Final Portfolio Value: {:.2f}'.format(cerebro.broker.getvalue()))

    # cerebro.plot()


if __name__ == '__main__':
    runstrat()