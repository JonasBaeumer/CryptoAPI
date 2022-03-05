import pandas as pd
import matplotlib.pyplot as plt


class Account_balance_graph(object):
    filepath = None

    def __init__(self, filepath):
        self.filepath = filepath

    """
    This method takes the data from a given csv file and generates a graph to visualize the progress of the account balance
    :param 
    :return: None, It writes a graph and stores it at the file storage place
    """

    def create_acc_balance_graph(self):
        # reading the CSV file
        # csv_file = pd.read_csv(self.filepath, index_col=0, parse_dates=True)
        csv_file = pd.read_csv(self.filepath, index_col=0)

        # displaying the contents of the CSV file
        print(csv_file)

        # Get a subset without the account number
        account_balance = csv_file[["balance", "currency"]]

        print(account_balance)

        graph1 = account_balance.plot()
        plt.savefig("C:/Users/jbaeu/OneDrive/Desktop/Trading/Trading Journal/accumulated_account_balance.png")
