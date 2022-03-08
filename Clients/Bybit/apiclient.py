import bybit

"""
Contains the general method/structure to make request to the API
For documentation visit: https://bybit-exchange.github.io/docs/inverse/#t-introduction 
"""


class APIClient:
    client = None

    MAIN_NET_API_URL = 'https://api-testnet.bybit.com'
    TEST_NET_API_URL = 'https://api.bybit.com'

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

    def __init__(self, api_key, api_secret):
        client = bybit.bybit(test=False, api_key=api_key, api_secret=api_secret)

    def get_account_balance(self):
        None
