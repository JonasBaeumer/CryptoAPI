from Phemex.JournalWriter.writer import Writer

#TODO: CLASS CAN BE REMOVED AFTER TESTING
if __name__ == '__main__':
    writer = Writer("C:/Users/jbaeu/OneDrive/Desktop/Trading/Trading Journal/data.csv")
    # :param data: [date,account_number,balance,currency]
    data = ['02.02.2022', '012648673246', '20', 'BTC']
    writer._write_to_csv_file(data)

