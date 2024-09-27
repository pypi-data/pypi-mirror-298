import backtrader as bt
from datetime import datetime
import os
import requests
import json
from backtrader.utils.py3 import queue
from backtrader.utils import AutoOrderedDict
import threading
import time

__ALL__ = ['MyBroker']

class MyBroker(bt.BrokerBase):

    def __init__(self, id=None, debug=False, *args, **kwargs):
        super(MyBroker, self).__init__(*args, **kwargs)
        self.base_url = os.environ.get('MY_BROKER_BASE_URL', 'http://192.168.25.247:8220')
        self.id = id if id is not None else os.environ.get('MY_BROKER_ID', "14282761")
        self.cash = None
        self.orders = {}
        self.notifs = queue.Queue()
        self.debug = debug

    def getcash(self):
        url = self.base_url + f"/balance/tv/{self.id}"
        response = requests.get(url).json()
        if response.get('code') == "200":
            self.cash = response['results']['balance']

        return self.cash

    def getvalue(self, datas=None):
        value = self.cash
        url = self.base_url + f"/positions/tv/{self.id}"
        response = requests.get(url).json()

        if response.get('code') == "200":
            for pos in response['results']:
                if pos['tradeSide'] == 'buy':
                    value = value + pos['qty'] * (pos['latestPrice'] - pos['avgPrice'])
                elif pos['tradeSide'] == 'sell':
                    value = value + pos['qty'] * (pos['avgPrice'] - pos['latestPrice'])

        return value

    def getposition(self, data):
        url = self.base_url + f"/positions/tv/{self.id}"
        response = requests.get(url).json()

        position = bt.Position()
        if response.get('code') == "200":
            for pos in response['results']:
                if pos['symbol'] == data.p.symbol:
                    position = bt.Position(size=pos['qty'] if pos['tradeSide'] == 'buy' else -pos['qty'], price=pos['avgPrice'])
                    break
        return position

    def cancel(self, order_id):
        url = self.base_url + f"/cancel/order/tv/{self.id}"
        data = {
            "tradeId": order_id,
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

        order_id = None
        if response.get('code') == "200":
            order_id = response['results']
            order.status = bt.Order.Submitted
            order.ref = order_id
            info = AutoOrderedDict()
            info.symbol = order.data.p.symbol
            order.info = info

            self.orders[order_id] = order

        return order_id

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
            return None

    def next(self):
        trade_ids = []
        for order_id, order in self.orders.items():
            if order.status != bt.Order.Completed and order.status != bt.Order.Cancelled:
                trade_ids.append(order_id)

        if len(trade_ids) > 0:
            url = self.base_url + f"/orders/query/tv/{self.id}"
            data = {
                "tradeIdList": trade_ids
            }
            payload = f"content={json.dumps(data)}"
            headers = {
                'Content-Type': 'application/x-www-form-urlencoded'
            }

            response = requests.post(url, headers=headers, data=payload).json()
            if response.get('code') == "200":
                for item in response['results']:
                    item_status = None
                    if item['orderStatus'] == "pending" or item['orderStatus'] == "working":
                        item_status = bt.Order.Submitted
                    elif item['orderStatus'] == "cancelled":
                        item_status = bt.Order.Cancelled
                    elif item['orderStatus'] == "filled":
                        item_status = bt.Order.Completed

                    order = self.orders.get(item['tradeId'], None)
                    if order is not None and order.status != item_status:
                        if self.debug:
                            print(f"MyBroker, next, order status changed, orderId: {order.ref}, old status: {order.getstatusname()}, new status: {bt.Order.Status[item_status]}")
                        
                        if item_status == bt.Order.Completed:
                            order.executed.size = item['qty']
                            order.executed.price = item['executePrice']

                        order.status = item_status
                        self.orders[item['tradeId']] = order
                        self.notifs.put(order.clone())