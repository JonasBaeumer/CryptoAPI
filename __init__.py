from Phemex.phemexclient import PhemexClient

if __name__ == '__main__':
    test_client = PhemexClient()
    test_client.get_account_balance()

