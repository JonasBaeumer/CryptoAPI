from Phemex.apiclient import APIClient
import linecache
import os
import sys
import time

dir_path = os.path.dirname(os.path.realpath(__file__))
sys.path.append(dir_path + "/../")


class PhemexClient(object):

    api_keys = ['0']
    api_secrets = ['0']
    client_main = None
    client_swing = None
    doc_size = None
    doc_path = '/Users/jonasb./PycharmProjects/PhemexAPI/data'

    def __init__(self):
        self.client_main = APIClient(self.api_key_main, self.api_secret_main)  # -> MainNetClient
        self.client_swing = APIClient(self.api_key_swing, self.api_secret_swing)
        self.doc_size = rawcount('/Users/jonasb./PycharmProjects/PhemexAPI/data')
        for i in range(1, int(self.doc_size), 3):
            self.api_keys.append(linecache.getline(self.doc_path, i + 1).rstrip("\n"))
            self.api_secrets.append(linecache.getline(self.doc_path, i + 2).rstrip("\n"))

    def get_Account_Balance(self):
        # Get account and positions for Main Account
        response_btc_main = self.client_main.query_account_n_positions(APIClient.CURRENCY_BTC)
        response_usd_main = self.client_main.query_account_n_positions(APIClient.CURRENCY_USD)

        # Get account and position for SWING Account
        response_btc_swing = self.client_swing.query_account_n_positions(APIClient.CURRENCY_BTC)
        response_usd_swing = self.client_swing.query_account_n_positions(APIClient.CURRENCY_USD)
        """
        From the official documentation:
        -> Fields with post-fix "Ev" are scaled values
        E.g. the account balance is written in Satoshis (1 BTC = 100.000.000 sats) 
        """

        balance_btc_main_contract = (response_btc_main.get('data', 'no entry found') \
                                     .get('account', 'no entry found') \
                                     .get('accountBalanceEv', 'no entry found') / 100000000)

        balance_usd_main_contract = (response_usd_main.get('data', 'no entry found') \
                                     .get('account', 'no entry found') \
                                     .get('accountBalanceEv', 'no entry found') / 10000)

        print("The BTC account balance (Contract) is: " + str(balance_btc_main_contract))
        print("The USD account balance (Contract) is: " + str(balance_usd_main_contract))

        balance_btc_swing_contract = (response_btc_swing.get('data', 'no entry found') \
                                      .get('account', 'no entry found') \
                                      .get('accountBalanceEv', 'no entry found') / 100000000)

        balance_usd_swing_contract = (response_usd_swing.get('data', 'no entry found') \
                                      .get('account', 'no entry found') \
                                      .get('accountBalanceEv', 'no entry found ') / 10000)

        print("The BTC account balance (Contract) is: " + str(balance_btc_swing_contract))
        print("The USD account balance (Contract) is: " + str(balance_usd_swing_contract))

        try:
            r = self.client.query_account_n_positions("BTC1")
            print(r)
        except APIClient.phemexexception.exceptions.PhemexAPIException as e:
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
        except APIClient.phemexexception.exceptions.PhemexAPIException as e:
            print(e)

        # Send replace if this order not filled yet
        try:
            response = self.client.amend_order(APIClient.SYMBOL_BTCUSD, ordid, {"priceEp": 95500000})
            print("response:" + str(response))
        except APIClient.phemexexception.exceptions.PhemexAPIException as e:
            print(e)

    def cancel_single_order(self):
        # Cancel one order
        try:
            r = self.client.cancel_order(APIClient.SYMBOL_BTCUSD, "ordid -> Insert Ord ID here")
            print("response:" + str(r))
        except APIClient.phemexexception.exceptions.PhemexAPIException as e:
            print(e)

    def cancel_all_active_orders(self):
        # Cancel all active orders
        try:
            self.client.cancel_all_normal_orders(APIClient.SYMBOL_BTCUSD)
        except APIClient.phemexexception.exceptions.PhemexAPIException as e:
            print(e)

    def cancel_all_conditional_orders(self):
        # Cancel all conditional orders
        try:
            self.client.cancel_all_untriggered_conditional_orders(APIClient.SYMBOL_BTCUSD)
        except APIClient.phemexexception.exceptions.PhemexAPIException as e:
            print(e)

    def cancel_all_orders(self):
        # Cancel all orders
        try:
            self.client.cancel_all(APIClient.SYMBOL_BTCUSD)
        except APIClient.phemexexception.exceptions.PhemexAPIException as e:
            print(e)

    def set_leverage(self):
        # Set leverage
        try:
            # Set 0 to change back to cross margin
            # Set to 10x
            r = self.client.change_leverage(APIClient.SYMBOL_BTCUSD, 10)
            print("response:" + str(r))
        except APIClient.phemexexception.exceptions.PhemexAPIException as e:
            print(e)

    def set_risk_limit(self):  # TODO SET FOR 150 BTC
        # Set risklimit for 150 BTC
        try:
            r = self.client.change_risklimit(APIClient.SYMBOL_BTCUSD, 150)
            print("response:" + str(r))
        except APIClient.phemexexception.exceptions.PhemexAPIException as e:
            print(e)

    def get_all_active_orders(self):
        # Get all active orders
        try:
            r = self.client.query_open_orders(APIClient.SYMBOL_BTCUSD)
            print("response:" + str(r))
        except APIClient.phemexexception.exceptions.PhemexAPIException as e:
            print(e)

        try:
            print(self.client.query_24h_ticker("BTCUSD"))
        except APIClient.phemexexception.exceptions.PhemexAPIException as e:
            print(e)


########## HELPER METHODS BELOW #########

def rawcount(filename):
    """
    FROM https://stackoverflow.com/questions/845058/how-to-get-line-count-of-a-large-file-cheaply-in-python
    Works faster with byte counters (only Python3) than traditional line counting methods

    :param filename: (str) - full file path
    :returns number of lines the document has
    """
    f = open(filename, 'rb')
    lines = 0
    buf_size = 1024 * 1024
    read_f = f.raw.read

    buf = read_f(buf_size)
    while buf:
        lines += buf.count(b'\n')
        buf = read_f(buf_size)

    return lines + 1 #Because lastline does not have line seperator
