from Phemex.phemexclient import PhemexClient
from Phemex.apiclient import APIClient

if __name__ == '__main__':
    test_client = PhemexClient()
    test_client.get_Account_Balance()

