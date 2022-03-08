import csv
from datetime import datetime
from datetime import date

from Clients.Phemex.apiclient import APIClient
from Clients.Phemex.phemexexception.exceptions import PhemexAPIException
from DataProcessing.JournalWriter.writer import Writer
import linecache
import os
import sys
import time

dir_path = os.path.dirname(os.path.realpath(__file__))
sys.path.append(dir_path + "/../")


class PhemexClient(object):
    api_keys = ['0']
    api_secrets = ['0']
    clients = [APIClient()]
    doc_size = None
    data_doc_path = 'C:/Users/jbaeu/OneDrive/Desktop/Trading/Trading Journal/phemex_login_data.csv'
    account_balance_doc_path = 'C:/Users/jbaeu/OneDrive/Desktop/Trading/Trading Journal/accumulated_account_balance.csv'

    def __init__(self):
        self.doc_size = rawcount(self.data_doc_path)
        for i in range(0, int(self.doc_size)):
            api_key = linecache.getline(self.data_doc_path, i+1).rstrip("\n")
            api_secret = linecache.getline(self.data_doc_path, i+2).rstrip("\n")
            self.api_keys.append(api_key)
            self.api_secrets.append(api_secret)
            self.clients.append(APIClient(api_key, api_secret))
        self.api_keys.remove('0')
        self.api_secrets.remove('0')
        self.clients.pop(0)

    def get_account_balance(self):
        """
        Writes the retrieved account balance into a csv file for further processing
        :return: None
        """

        for i in range(len(self.clients)):
            response_client_btc = self.clients[i].query_account_n_positions(APIClient.CURRENCY_BTC)
            response_client_usd = self.clients[i].query_account_n_positions(APIClient.CURRENCY_USD)
            account_number = response_client_btc.get('data').get('account').get('accountId')
            """
            From the official documentation:
            -> Fields with post-fix "Ev" are scaled values
            E.g. the account balance is written in Satoshis (1 BTC = 100.000.000 sats) 
            """
            btc_balance = response_client_btc.get('data').get('account').get('accountBalanceEv') / 100000000
            btc_client = response_client_btc.get('data').get('account')
            usd_balance = response_client_usd.get('data').get('account').get('accountBalanceEv') / 10000 #usd_balance currently not in use
            print('ACCOUNT BALANCES FOR ACC.NR ' + str(account_number))
            print('BTC: ' + str(btc_balance))
            print('USD: ' + str(usd_balance))

            write_to_csv(self.account_balance_doc_path, data=[date.today().strftime("%d.%m.%Y"),
                                                              str(account_number), str(btc_balance), 'BTC'])
            try:
                r = response_client_btc
                print(r)
            except PhemexAPIException as e:
                print(e)

    # Place a new order, priceEp is scaled price, check our API doc for more info about scaling
    # https://github.com/phemex/phemex-api-docs/blob/master/Public-API-en.md#scalingfactors

    def place_Order(self):
        try:
            response = self.client.place_order({
                "symbol": APIClient.SYMBOL_BTCUSD,
                "clOrdID": "JackTest1" + str(time.time()),
                "side": APIClient.SIDE_BUY,
                "orderQty": 10,
                "priceEp": 95000000,
                "ordType": APIClient.ORDER_TYPE_LIMIT,
                "timeInForce": APIClient.TIF_GOOD_TILL_CANCEL})
            print("response:" + str(response))
            ordid = response["data"]["orderID"]
            print(ordid)
        except PhemexAPIException as e:
            print(e)

        # Send replace if this order not filled yet
        try:
            response = self.client.amend_order(APIClient.SYMBOL_BTCUSD, ordid, {"priceEp": 95500000})
            print("response:" + str(response))
        except PhemexAPIException as e:
            print(e)

    def cancel_single_order(self):
        # Cancel one order
        try:
            r = self.client.cancel_order(APIClient.SYMBOL_BTCUSD, "ordid -> Insert Ord ID here")
            print("response:" + str(r))
        except PhemexAPIException as e:
            print(e)

    def cancel_all_active_orders(self):
        # Cancel all active orders
        try:
            self.client.cancel_all_normal_orders(APIClient.SYMBOL_BTCUSD)
        except PhemexAPIException as e:
            print(e)

    def cancel_all_conditional_orders(self):
        # Cancel all conditional orders
        try:
            self.client.cancel_all_untriggered_conditional_orders(APIClient.SYMBOL_BTCUSD)
        except PhemexAPIException as e:
            print(e)

    def cancel_all_orders(self):
        # Cancel all orders
        try:
            self.client.cancel_all(APIClient.SYMBOL_BTCUSD)
        except PhemexAPIException as e:
            print(e)

    def set_leverage(self):
        # Set leverage
        try:
            # Set 0 to change back to cross margin
            # Set to 10x
            r = self.client.change_leverage(APIClient.SYMBOL_BTCUSD, 10)
            print("response:" + str(r))
        except PhemexAPIException as e:
            print(e)

    def set_risk_limit(self):  # TODO SET FOR 150 BTC
        # Set risklimit for 150 BTC
        try:
            r = self.client.change_risklimit(APIClient.SYMBOL_BTCUSD, 150)
            print("response:" + str(r))
        except PhemexAPIException as e:
            print(e)

    def get_all_active_orders(self):
        # Get all active orders
        try:
            r = self.client.query_open_orders(APIClient.SYMBOL_BTCUSD)
            print("response:" + str(r))
        except PhemexAPIException as e:
            print(e)

        try:
            print(self.client.query_24h_ticker("BTCUSD"))
        except PhemexAPIException as e:
            print(e)

    def get_trade_history(self):

        for i in range(len(self.clients)):

            try:
                r = self.clients[i].query_closed_orders("BTCUSD", 0, datetime.now().timestamp(), 1000000000000000, 1000000000000000, "Filled")
                print("response:" + str(r))
            except PhemexAPIException as e:
                print(e)



########## HELPER METHODS BELOW #########

def rawcount(filename):
    """
    FROM https://stackoverflow.com/questions/845058/how-to-get-line-count-of-a-large-file-cheaply-in-python
    Works faster with byte counters (only Python3) than traditional line counting methods

    :param filename: (str) - full file path
    :returns number of lines the document has
    """
    with open(filename, 'r+', encoding='UTF-8', newline='') as file:
        reader = csv.reader(file, delimiter="\n")
        data_from_file = list(reader)
        return len(data_from_file) - 1


def write_to_csv(filepath, data=[]):
    writer_client = Writer(filepath)
    return_value = writer_client._write_to_csv_file(data)
    return return_value
