import bybit

"""
Contains the general method/structure to make request to the API
For documentation visit: https://bybit-exchange.github.io/docs/inverse/#t-introduction 
"""


class APIClient:
    client = None

    MAIN_NET_API_URL = 'https://api-testnet.bybit.com'
    TEST_NET_API_URL = 'https://api.bybit.com'

    def __init__(self, api_key, api_secret):
        client = bybit.bybit(test=False, api_key=api_key, api_secret=api_secret)

    def get_account_balance(self):
        None

    def get_server_time(self):
        """
        https://campus.tum.de/tumonline/pl/ui/$ctx;design=pl;header=max;lang=de/wbLv.wbShowLVDetail?pStpSpNr=950604891&pSpracheNr=1
        :return: (int) bybit server time - required for server requests
        """
        return self.client.Common.Common_getTime().result()[0]
