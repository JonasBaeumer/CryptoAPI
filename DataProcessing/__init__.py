from DataProcessing.Graphs.account_balance_graph import Account_balance_graph

if __name__ == '__main__':
    test1 = Account_balance_graph(
        "C:/Users/jbaeu/OneDrive/Desktop/Trading/Trading Journal/accumulated_account_balance.csv")
    test1.create_acc_balance_graph()
