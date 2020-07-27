import backtrader as bt
import backtrader.feeds as btfeeds
import backtrader.indicators as btind
import data_formats
import datetime

class ReversalStrategy(bt.Strategy):
    def __init__(self):
        self.dataclose = self.datas[0].close

        self.bbands = btind.BollingerBands(period=20,devfactor=2)

        self.stoch = btind.Stochastic(period=14,period_dfast=3,period_dslow=3)

        self.orders = list()

        self.short_signal = bt.And(self.dataclose > self.bbands.top, self.stoch.percK > 80)

        self.long_signal = bt.And(self.dataclose < self.bbands.bot, self.stoch.percK < 20)

        self.close_long_signal = self.dataclose >= self.bbands.top

        self.close_short_signal = self.dataclose <= self.bbands.bot

        self.loss_perc = 0.025

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

        self.orders.remove(order)

    def notify_trade(self, trade):
        if not trade.isclosed:
            return

        self.log('OPERATION PROFIT, GROSS {:.2f}, NET {:.2f}, CASH: {:.2f}'.format(trade.pnl, trade.pnlcomm, self.broker.get_cash()))
                    

    def log(self, txt):
        dt = self.data.datetime.datetime()
        print(dt, txt)


    def next(self):
        # Do not hold overnight, refactor this into a func
        if self.position.size != 0:
            if self.data.datetime.time() > datetime.time(15,30):
                if self.position.size > 0:
                    mkt_sell = self.close(oco=self.orders[0])
                    self.orders.append(mkt_sell)
                    self.log('SELL CREATE CLOSE, Price: {}, QTY: {}'.format(self.dataclose[0],mkt_sell.size))

                elif self.position.size < 0:
                    mkt_buy = self.close(oco=self.orders[0])
                    self.orders.append(mkt_buy)
                    self.log('BUY CREATE CLOSE, Price: {}, QTY: {}'.format(self.dataclose[0],mkt_buy.size))

        if len(self.orders) > 1:
            return
        elif len(self.orders) == 1:
            if self.position.size > 0 and self.close_long_signal[0] == True:
                mkt_sell = self.close(oco=self.orders[0])
                self.orders.append(mkt_sell)
                self.log('SELL CREATE CLOSE, Price: {}, QTY: {}'.format(self.dataclose[0],mkt_sell.size))

            elif self.position.size < 0 and self.close_short_signal[0] == True:
                mkt_buy = self.close(oco=self.orders[0])
                self.orders.append(mkt_buy)
                self.log('BUY CREATE CLOSE, Price: {}, QTY: {}'.format(self.dataclose[0],mkt_buy.size))

        if not self.position:
            if self.long_signal[0] == True:
                mkt_buy = self.buy(size=self.pos_size(), exectype=bt.Order.Market, transmit=False)
                stp_sell = self.sell(price=self.stop_price(mkt_buy.isbuy()),size=mkt_buy.size, exectype=bt.Order.Stop, transmit=True,parent=mkt_buy)
                self.orders.extend([mkt_buy,stp_sell])
                self.log('BUY CREATE, Price: {}, QTY: {}, Stop:{}'.format(self.dataclose[0],mkt_buy.size,stp_sell.price))

            elif self.short_signal[0] == True:
                mkt_sell = self.sell(size=self.pos_size(), exectype=bt.Order.Market, transmit=False)
                stp_buy = self.buy(price=self.stop_price(mkt_sell.isbuy()),size=mkt_sell.size, exectype=bt.Order.Stop, transmit=True,parent=mkt_sell)
                self.orders.extend([mkt_sell,stp_buy])
                self.log('SELL CREATE, Price: {}, QTY: {}, Stop:{}'.format(self.dataclose[0],mkt_sell.size,stp_buy.price))


    def pos_size(self):
        maxS = (self.broker.get_cash() * 4 / self.dataclose[0])

        return int(maxS)
        # Update this with risk % when using multiple concurrent statergies / instruments


    def stop_price(self,dir):
        if dir == True:
            stoploss = self.dataclose[0] - self.dataclose[0] * self.loss_perc
        else:
            stoploss = self.dataclose[0] + self.dataclose[0] * self.loss_perc

        return round(stoploss,2)


def runstrat(datapath):
    cerebro = bt.Cerebro()

    data = data_formats.IEXMinuteCSV(dataname=datapath)

    cerebro.adddata(data)
    
    cerebro.addstrategy(ReversalStrategy)

    cerebro.broker.setcash(50000)
    cerebro.broker.setcommission(commission=0,leverage=4)
    
    print('Starting Portfolio Value: {:.2f}'.format(cerebro.broker.getvalue()))

    cerebro.run()

    print('Final Portfolio Value: {:.2f}'.format(cerebro.broker.getvalue()))

    cerebro.plot()


if __name__ == '__main__':
    runstrat('./data/SPY-202007-minute.csv')