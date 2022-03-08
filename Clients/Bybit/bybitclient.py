import csv
import linecache

from Clients.Bybit.apiclient import APIClient
from DataProcessing.JournalWriter.writer import Writer


class BybitClient:
    api_keys = ['0']
    api_secrets = ['0']
    clients = [APIClient()]
    doc_size = None
    data_doc_path = 'C:/Users/jbaeu/OneDrive/Desktop/Trading/Trading Journal/bybit_login_data.csv'
    account_balance_doc_path = 'C:/Users/jbaeu/OneDrive/Desktop/Trading/Trading Journal/accumulated_account_balance.csv'

    """
    Contains the logic and implementation to use API requests to Bybit
    """

    def __init__(self):
        self.doc_size = rawcount(self.data_doc_path)
        for i in range(0, int(self.doc_size)):
            api_key = linecache.getline(self.data_doc_path, i + 1).rstrip("\n")
            api_secret = linecache.getline(self.data_doc_path, i + 2).rstrip("\n")
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
            response = None

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