from Phemex.JournalWriter.writer import Writer

if __name__ == '__main__':
    writer = Writer("C:/Users/jbaeu/OneDrive/Desktop/Trading/Trading Journal/data.csv")
    # :param data: [date,account_number,balance,currency]
    data = ['12.02.20XXXX00', '012648673246', '20', 'BTC']
    writer._write_to_csv_file(data)

