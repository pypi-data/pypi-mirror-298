import backtrader as bt
from datetime import datetime
import os
import requests
import json
from backtrader.utils.py3 import queue
import threading

__ALL__ = ['MyBroker']

class MyBroker(bt.BrokerBase):

    def __init__(self, id=None, cash=None, debug=False, *args, **kwargs):
        super(MyBroker, self).__init__(*args, **kwargs)
        self.base_url = os.environ.get('MY_BROKER_BASE_URL', 'http://192.168.25.247:8220')
        self.id = id if id is not None else os.environ.get('MY_BROKER_ID', "14282761")
        self.cash = cash
        self.orders = {}
        self.notifs = queue.Queue()
        self.order_status_thread = None
        self.debug = debug

    def start(self):
        super(MyBroker, self).start()

        self.order_status_thread = threading.Thread(target=self.order_status_worker, args=(self,))

        # url = self.base_url + f"/orders/query/tv/{self.id}"
        # data = {}
        # payload = f"content={json.dumps(data)}"

        # if self.debug:
        #     print(f"start, payload: {payload}")

        # headers = {
        #     'Content-Type': 'application/x-www-form-urlencoded'
        # }

        # response = requests.post(url, headers=headers, data=payload).json()
        # if self.debug:
        #     print(f"start, response: {response}")

        # if response.get('code') == "200":
        #     for order in response['results']:
        #         if order['orderStatus'] == "pending" or order['orderStatus'] == "working":
        #             if self.debug:
        #                 print(f"start, order: {order}")
        #             o = None
        #             if order['tradeSide'] == 'buy':
        #                 o = bt.order.BuyOrder(data=self.data, size=order['qty'], price=order['allocationPrice'], exectype=order['orderType'])
        #             elif order['tradeSide'] == 'sell':
        #                 o = bt.order.SellOrder(data=self.data, size=order['qty'], price=order['allocationPrice'], exectype=order['orderType'])

        #             if o is not None:
        #                 o.ref = order['tradeId']
        #                 o.exectype = bt.Order.Market if order['orderType'] == 'market' else bt.Order.Limit
        #                 o.status = bt.Order.Submitted 
        #                 o.status = order['qty']
        #                 o.price = order['executePrice']
        #                 o.pricelimit = order['allocationPrice'] if order['orderType'] == 'limit' else None
        #                 info = AutoOrderedDict()
        #                 info.symbol = order['symbol']
        #                 o.info = info
        #                 self.orders[o.ref] = o
        #                 self.notifs.put(o)

    def order_status_worker(self):
        while True:
            for order_id, order in self.orders.items():
                pass

    def stop(self):
        super(MyBroker, self).stop()

    def getcash(self):
        url = self.base_url + f"/balance/tv/{self.id}"
        response = requests.get(url).json()
        if self.debug:
            print(f"getcash, response: {response}")

        if response.get('code') == "200":
            self.cash = response['results']['balance']

        return self.cash

    def getvalue(self, datas=None):
        value = self.cash
        url = self.base_url + f"/positions/tv/{self.id}"
        response = requests.get(url).json()
        if self.debug:
            print(f"getvalue, response: {response}")

        if response.get('code') == "200":
            for pos in response['results']:
                if self.debug:
                    print(f"getvalue, pos: {pos}")
                if pos['tradeSide'] == 'buy':
                    value = value + pos['qty'] * (pos['latestPrice'] - pos['avgPrice'])
                elif pos['tradeSide'] == 'sell':
                    value = value + pos['qty'] * (pos['avgPrice'] - pos['latestPrice'])

        if self.debug:
            print(f"getvalue, value: {value}")

        return value

    def getposition(self, data):
        url = self.base_url + f"/positions/tv/{self.id}"
        response = requests.get(url).json()
        if self.debug:
            print(f"getposition, response: {response}")

        position = bt.Position()
        if response.get('code') == "200":
            for pos in response['results']:
                if pos['symbol'] == data.p.symbol:
                    position = bt.Position(size=pos['qty'] if pos['tradeSide'] == 'buy' else -pos['qty'], price=pos['avgPrice'])
                    break
        return position

    def cancel(self, orderId):
        url = self.base_url + f"/cancel/order/tv/{self.id}"
        data = {
            "tradeId": orderId,
        }
        payload = f"content={json.dumps(data)}"
        if self.debug:
            print(f"cancel, payload: {payload}")

        headers = {
            'Content-Type': 'application/x-www-form-urlencoded'
        }

        response = requests.post(url, headers=headers, data=payload).json()
        if self.debug:
            print(f"cancel, response: {response}")
        return response

    def submit(self, order, **kwargs):
        url = self.base_url + f"/place/order/tv/{self.id}"

        data = {
            "symbol": order.data.p.symbol,
            "side": kwargs['side'],
            "qty": order.size,
            "price": order.price,
            "type": "market" if order.exectype == bt.Order.Market else "limit",
        }
        payload = f"content={json.dumps(data)}"
        if self.debug:
            print(f"submit, payload: {payload}")

        headers = {
            'Content-Type': 'application/x-www-form-urlencoded'
        }

        response = requests.post(url, headers=headers, data=payload).json()
        if self.debug:
            print(f"submit, response: {response}")

        orderId = None
        if response.get('code') == "200":
            orderId = response['results']
            order.status = bt.Order.Submitted
            order.ref = orderId

            self.orders[orderId] = order
            self.notifs.put(order)

        return orderId

    def buy(self, owner, data, size, price=None, plimit=None, exectype=None, valid=None, tradeid=0, oco=None, trailamount=None, trailpercent=None, **kwargs):
        order = bt.order.BuyOrder(owner=owner, data=data, size=size, price=price, pricelimit=plimit, exectype=exectype, valid=valid, tradeid=tradeid, oco=oco, trailamount=trailamount, trailpercent=trailpercent)
        return self.submit(order, **kwargs)

    def sell(self, owner, data, size, price=None, plimit=None, exectype=None, valid=None, tradeid=0, oco=None, trailamount=None, trailpercent=None, **kwargs):
        order = bt.order.SellOrder(owner=owner, data=data, size=size, price=price, pricelimit=plimit, exectype=exectype, valid=valid, tradeid=tradeid, oco=oco, trailamount=trailamount, trailpercent=trailpercent)
        return self.submit(order, **kwargs)
    
    def get_notification(self):
        try:
            return self.notifs.get(False)
        except queue.Empty:
            pass

        return None

    def next(self):
        pass
