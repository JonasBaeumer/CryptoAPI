import bybit

"""
For documentation visit: https://bybit-exchange.github.io/docs/inverse/#t-introduction 
"""


class BybitClient:
    client = None

    def __init__(self, api_key, api_secret):
        client = bybit.bybit(test=True, api_key=api_key, api_secret=api_secret)

    def get_account_balance(self):
        None
