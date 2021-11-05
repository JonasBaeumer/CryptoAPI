import hashlib
import hmac
from threading import Thread
import requests
import json


def getP_and_L():
    """
    Retrieve the P&L Data from the Server
    """
    website_path = "https://api.phemex.com/"
    request_path = "accounts/accountPositions"
    message = '{} {} {}'.format(website_path, request_path, "hello") # Example how to get it in json format
    API_Secret = None
    signature = hmac.new(bytes(API_Secret, 'latin-1'), msg = bytes(message, 'latin-1'), digestmod=hashlib.sha256()).hexdigest().upper()
    Header = RequestObjectHeader(None, 1575735514, signature)

    try:
        # data contains the request body
        response = requests.get(website_path + request_path + "?currency=BTC", headers = {}, data = {}).

        if response.status_code != 200:
            update_lb = True



class RequestObject(object):

    def __int__(self):
        self.__header = None
        self.__body = None

class RequestObjectHeader(object):

    def __init__(self, accesstoken, expiry, signature):
        self.__x_phemex_access_token = accesstoken
        self.__x_phemex_request_expiry = expiry  # Usually (Now() + 1 minute)
        self.__x_phemex_request_signature = signature # HMAC SHA256(URL PATH + Query String + Expiry + body)

        """
        Optional header
        self.__x_phemex_request_tracing = None # Uniqure String to trace Http Requests (< 40 bytes)
        """



if __name__ == '__main__':
