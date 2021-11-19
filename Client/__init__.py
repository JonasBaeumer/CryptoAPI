import hashlib
import hmac
from math import trunc
import json
import time

from Client.phemexexception.exceptions import PhemexAPIException


class Client(object):
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

    def getP_and_L(self):
        """
        Retrieve the P&L Data from the Server
        """
        website_path = "https://api.phemex.com"
        request_path = "/accounts/accountPositions"
        pair_path = "currency=BTC"
        expiry = 1575735514
        message = '{} {} {}'.format(website_path, request_path, "hello")  # Example how to get it in json format
        API_Secret = None
        signature = hmac.new(bytes(request_path + pair_path + expiry, 'latin-1'), msg=bytes(message, 'latin-1'),
                             digestmod=hashlib.sha256()).hexdigest().upper()

    """ BELOW WILL BE SOME INITIAL METHODS FOR TESTING THE SECURITY ENDPOINTS ACCESS"""

    def get_Balance_Test(self):
        """
        :return: The Current Account Balance in BTC
        """
        website_path = "https://api.phemex.com"
        request_path = "/accounts/accountPositions"
        request_query = "currency=BTC"
        expiry = 1575735514
        message = ""
        signature = hmac.new(bytes(request_path + request_query + expiry, 'latin-1'), msg=bytes(message, 'latin-1'),
                             digestmod=hashlib.sha256()).hexdigest().upper()
        print(self._send_request("GET", request_path, request_query, body={}))


if __name__ == '__main__':
    Test_Client = Client()
    Test_Client.get_Balance_Test()
