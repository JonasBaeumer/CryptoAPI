import linecache
import os
import sys
import time

dir_path = os.path.dirname(os.path.realpath(__file__))
sys.path.append(dir_path + "/../")

import Client
from .phemexexception import exceptions

class Client(object):

    api_key = None
    api_secret = None
    client = None

    def __init__(self):
        self.api_key = linecache.getline('/Users/jonasb./PycharmProjects/PhemexAPI/data', 1).rstrip("\n")
        self.api_secret = linecache.getline('/Users/jonasb./PycharmProjects/PhemexAPI/data', 2).rstrip("\n")
        self.client = Client(self.api_key, self.api_secret, True) # -> TESTNET CLIENT


    def __get_Account_Balance(self):
        # Get account and positions
        balancebtc = self.client.query_account_n_positions(Client.CURRENCY_BTC)
        balanceusd = self.client.query_account_n_positions(Client.CURRENCY_USD)
        print("The accounts BTC balance is: " + balancebtc)
        print("The accounts BTC balance is: " + balanceusd)

        try:
            r = self.client.query_account_n_positions("BTC1")
            print(r)
        except Client.phemexexception.exceptions.PhemexAPIException as e:
            print(e)

# Place a new order, priceEp is scaled price, check our API doc for more info about scaling
# https://github.com/phemex/phemex-api-docs/blob/master/Public-API-en.md#scalingfactors

    def __place_Order(self):
        try:
            response = self.client.place_order({
            "symbol":Client.SYMBOL_BTCUSD,
            "clOrdID":"JackTest1" + str(time.time()),
            "side":Client.SIDE_BUY,
            "orderQty":10,
            "priceEp": 95000000,
            "ordType":Client.ORDER_TYPE_LIMIT,
            "timeInForce" : Client.TIF_GOOD_TILL_CANCEL})
            print("response:" + str(r))
            ordid = response["data"]["orderID"]
            print(ordid)
        except Client.phemexexception.exceptions.PhemexAPIException as e:
            print(e)

        # Send replace if this order not filled yet
        try:
            response = self.client.amend_order(
                Client.SYMBOL_BTCUSD,
                ordid,
                {"priceEp": 95500000})
            print("response:" + str(r))
        except Client.phemexexception.exceptions.PhemexAPIException as e:
            print(e)

    def __cancel_single_order(self):
        # Cancel one order
        try:
            r = self.client.cancel_order(
                Client.SYMBOL_BTCUSD,
                ordid)
            print("response:" + str(r))
        except Client.phemexexception.exceptions.PhemexAPIException as e:
            print(e)

    def __cancel_all_active_orders(self):
        # Cancel all active orders
        try:
            self.client.cancel_all_normal_orders(Client.SYMBOL_BTCUSD)
        except Client.phemexexception.exceptions.PhemexAPIException as e:
            print(e)

    def __cancel_all_conditional_orders(self):
        # Cancel all conditional orders
        try:
            self.client.cancel_all_untriggered_conditional_orders(Client.SYMBOL_BTCUSD)
        except Client.phemexexception.exceptions.PhemexAPIException as e:
            print(e)

    def __cancel_all_orders(self):
        # Cancel all orders
        try:
            self.client.cancel_all(Client.SYMBOL_BTCUSD)
        except Client.phemexexception.exceptions.PhemexAPIException as e:
            print(e)

    def __set_leverage(self):
        # Set leverage
        try:
            # Set 0 to change back to cross margin
            # Set to 10x
            r = self.client.change_leverage(Client.SYMBOL_BTCUSD, 10)
            print("response:" + str(r))
        except Client.phemexexception.exceptions.PhemexAPIException as e:
            print(e)

    def __set_risk_limit(self): #TODO SET FOR 150 BTC
        # Set risklimit for 150 BTC
        try:
            r = self.client.change_risklimit(Client.SYMBOL_BTCUSD, 150)
            print("response:" + str(r))
        except Client.phemexexception.exceptions.PhemexAPIException as e:
            print(e)

    def __get_all_active_orders(self):
        # Get all active orders
        try:
            r = self.client.query_open_orders(Client.SYMBOL_BTCUSD)
            print("response:" + str(r))
        except Client.phemexexception.exceptions.PhemexAPIException as e:
            print(e)

        try:
            print(self.client.query_24h_ticker("BTCUSD"))
        except Client.phemexexception.exceptions.PhemexAPIException as e:
            print(e)