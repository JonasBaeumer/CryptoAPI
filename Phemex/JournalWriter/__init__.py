from Phemex.JournalWriter.writer import Writer

if __name__ == '__main__':
    writer = Writer("C:/Users/jbaeu/OneDrive/Desktop/Trading/Trading Journal")
    # :param data: [date,account_number,balance,currency]
    data = ['12.02.2000', '012648673246', '20', 'BTC']
    writer._write_to_csv_file_TEST(data)

