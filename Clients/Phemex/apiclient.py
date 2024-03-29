from Clients.Phemex.phemexexception.exceptions import PhemexAPIException
import hashlib
import hmac
from math import trunc
import json
import time

import requests


class APIClient(object):
    MAIN_NET_API_URL = 'https://api.phemex.com'
    TEST_NET_API_URL = 'https://testnet-api.phemex.com'

    CURRENCY_BTC = "BTC"
    CURRENCY_USD = "USD"

    SYMBOL_BTCUSD = "BTCUSD"
    SYMBOL_ETHUSD = "ETHUSD"
    SYMBOL_XRPUSD = "XRPUSD"

    SIDE_BUY = "Buy"
    SIDE_SELL = "Sell"

    ORDER_TYPE_MARKET = "Market"
    ORDER_TYPE_LIMIT = "Limit"

    TIF_IMMEDIATE_OR_CANCEL = "ImmediateOrCancel"
    TIF_GOOD_TILL_CANCEL = "GoodTillCancel"
    TIF_FOK = "FillOrKill"

    ORDER_STATUS_NEW = "New"
    ORDER_STATUS_PFILL = "PartiallyFilled"
    ORDER_STATUS_FILL = "Filled"
    ORDER_STATUS_CANCELED = "Canceled"
    ORDER_STATUS_REJECTED = "Rejected"
    ORDER_STATUS_TRIGGERED = "Triggered"
    ORDER_STATUS_UNTRIGGERED = "Untriggered"

    def __init__(self, api_key=None, api_secret=None, is_testnet=False):
        self.api_key = api_key
        self.api_secret = api_secret
        self.api_URL = self.MAIN_NET_API_URL
        if is_testnet:
            self.api_URL = self.TEST_NET_API_URL

        self.session = requests.session()

    def _send_request(self, method, endpoint, params={}, body={}):
        """
        A generic method to send a request to the Phemex API server
        :param method: POST, PUT, GET, DELETE
        :param endpoint: The endpoint that the requests it to be sent to
        :param params: Further define the api path regarding the request
        :param body: Specific data for the request (JSON Format)
        :return: JSON Message Object containing the details of the reply
        """

        # Get the current time for expiry
        expiry = str(trunc(time.time()) + 60)
        # Create the query string from the given method arguments
        query_string = '&'.join(['{}={}'.format(k, v) for k, v in params.items()])
        # Create the message for the signature encoding later
        message = endpoint + query_string + expiry
        # Create a message body in JSON format
        body_str = ""
        if body:
            body_str = json.dumps(body, separators=(',', ':'))
            message += body_str
        # Create the signature using the API secret plus message
        signature = hmac.new(self.api_secret.encode('utf-8'), message.encode('utf-8'), hashlib.sha256)

        # Update the request header (JSON)
        self.session.headers.update({
            'x-phemex-request-signature': signature.hexdigest(),
            'x-phemex-request-expiry': expiry,
            'x-phemex-access-token': self.api_key,
            'Content-Type': 'application/json'})

        url = self.api_URL + endpoint
        if query_string:
            url += '?' + query_string

        # Get and return the response from the Phemex API server
        response = self.session.request(method, url, data=body_str.encode())
        if not str(response.status_code).startswith('2'):
            raise PhemexAPIException(response)
        try:
            res_json = response.json()
        except ValueError:
            raise PhemexAPIException('Invalid Response: %s' % response.text)
        if "code" in res_json and res_json["code"] != 0:
            raise PhemexAPIException(response)
        if "error" in res_json and res_json["error"]:
            raise PhemexAPIException(response)
        return res_json

    def query_account_n_positions(self, currency: str):
        """
        https://github.com/phemex/phemex-api-docs/blob/master/Public-API-en.md#querytradeaccount
        """
        return self._send_request("get", "/accounts/accountPositions", {'currency': currency})

    def place_order(self, params={}):
        """
        https://github.com/phemex/phemex-api-docs/blob/master/Public-API-en.md#placeorder
        """
        return self._send_request("post", "/orders", body=params)

    def amend_order(self, symbol, orderID, params={}):
        """
        https://github.com/phemex/phemex-api-docs/blob/master/Public-API-en.md#622-amend-order-by-orderid
        """
        params["symbol"] = symbol
        params["orderID"] = orderID
        return self._send_request("put", "/orders/replace", params=params)

    def cancel_order(self, symbol, orderID):
        """
        https://github.com/phemex/phemex-api-docs/blob/master/Public-API-en.md#623-cancel-single-order
        """
        return self._send_request("delete", "/orders/cancel", params={"symbol": symbol, "orderID": orderID})

    def _cancel_all(self, symbol, untriggered_order=False):
        """
        https://github.com/phemex/phemex-api-docs/blob/master/Public-API-en.md#625-cancel-all-orders
        """
        return self._send_request("delete", "/orders/all",
                                  params={"symbol": symbol, "untriggered": str(untriggered_order).lower()})

    def cancel_all_normal_orders(self, symbol):
        self._cancel_all(symbol, untriggered_order=False)

    def cancel_all_untriggered_conditional_orders(self, symbol):
        self._cancel_all(symbol, untriggered_order=True)

    def cancel_all(self, symbol):
        self._cancel_all(symbol, untriggered_order=False)
        self._cancel_all(symbol, untriggered_order=True)

    def change_leverage(self, symbol, leverage=0):
        """
        https://github.com/phemex/phemex-api-docs/blob/master/Public-API-en.md#627-change-leverage
        """
        return self._send_request("PUT", "/positions/leverage", params={"symbol": symbol, "leverage": leverage})

    def change_risklimit(self, symbol, risk_limit=0):
        """
        https://github.com/phemex/phemex-api-docs/blob/master/Public-API-en.md#628-change-position-risklimit
        """
        return self._send_request("PUT", "/positions/riskLimit", params={"symbol": symbol, "riskLimit": risk_limit})

    def query_closed_orders(self, symbol, start, end, offset, limit, ordStatus):
        """
        :param symbol: (String) symbol that needs to be queried (f.e. <BTCUSD>)
        The epoch is the point where the time starts and is platform dependent. On Windows and most Unix systems,
        the epoch is January 1, 1970, 00:00:00 (UTC) and leap seconds are not counted towards the time in seconds since the epoch.
        :param start: (int) start time range, Epoch millis
        :param end: (int) end time range, Epoch millis
        offset is the difference to the current price (e.g. we set a range around the current price of trades that we want to see)

        :param offset: (int) offset to resultset
        :param limit: (int) limit of resultset
        :param ordStatus: (String) order status list filter (<New, Partially filled, Untriggered, Filled, Cancelled>)
        https://github.com/phemex/phemex-api-docs/blob/master/Public-API-en.md#6210-query-closed-orders-by-symbol
        """
        return self._send_request("GET", "/orders/activeList", params={"symbol": symbol, "start": start, "end": end,
                                                                       "offset": offset, "limit": limit, "ordstatus": ordStatus})

    def query_open_orders(self, symbol):
        """
        https://github.com/phemex/phemex-api-docs/blob/master/Public-API-en.md#6210-query-open-orders-by-symbol
        """
        return self._send_request("GET", "/orders/activeList", params={"symbol": symbol})

    def query_24h_ticker(self, symbol):
        """
        https://github.com/phemex/phemex-api-docs/blob/master/Public-API-en.md#633-query-24-hours-ticker
        """
        return self._send_request("GET", "/md/ticker/24hr", params={"symbol": symbol})


