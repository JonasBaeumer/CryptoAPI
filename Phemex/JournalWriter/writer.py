import csv
import datetime

"""
This class is supposed to handle all related issues with writing the recieved data from the phemex api to a specific file 
in a specific format.
"""

"""
WHAT TO DO:
A method that writes my desired data into the desired csv file: DONE!
"""


class Writer(object):
    filepath = None
    filepath_TEST = None

    def __init__(self, filepath):
        self.filepath = filepath
        self.filepath_TEST = "C:/Users/jbaeu/OneDrive/Desktop/Trading/Trading Journal"

    def _write_to_csv_file(self, data=[]):
        """
        This method takes a given data input and writes it into the desired csv file

        from https://www.pythontutorial.net/python-basics/python-write-csv-file/
        :param data: [date,account_number,balance,currency]
        :return: TRUE/FALSE (depending on writing success)
        """
        with open(self.filepath, 'r+', encoding='UTF-8', newline='') as file:
            """
            from: https://stackoverflow.com/questions/27504056/row-count-in-a-csv-file#:~:text=Then%20use%20the%20csv.reader%20for%20open%20the%20csv,%3D%20csv.reader%20%28input_file%29%20value%20%3D%20len%20%28list%20%28reader_file%29%29
            """
            reader = csv.reader(file, delimiter="\n")
            data_from_file = list(reader)
            row_count = len(data_from_file)

            # TODO: Delete later
            print(row_count)

        with open(self.filepath, 'a', encoding='UTF-8', newline='') as file:
            # TODO: Delete later
            print(self._string_to_list(data))

            if not self._check_for_duplicate_date_entry(data_from_file):

                file.write(self._string_to_list(data) + '\n')
                return True

        return False

    def _write_to_csv_file_TEST(self, data=[]):
        """
        from https://www.pythontutorial.net/python-basics/python-write-csv-file/
        :param data: [date,account_number,balance,currency]
        :return: TRUE/FALSE (depending on writing success)
        """
        with open(self.filepath_TEST, 'r+', encoding='UTF-8', newline='') as file:
            reader = csv.reader(file, delimiter='', quotechar='|')
            for row in reader:
                print(','.join(row))
            writer = csv.writer(file)
            writer.writerow(data)

        return True

    def _check_for_duplicate_date_entry(self, data=[]):
        """
        :param data: A list with rows from the csv file to be checked
        :return: TRUE/FALSE if the current date time is already saved as a row (to prevent duplicate entries)
        """

        current_date = datetime.datetime.now()
        date_string = datetime.date.strftime(current_date, '%d.%m.%Y')

        for i in range(0, len(data)):
            if date_string in data[i]:
                return True

        return False

    def _string_to_list(self, data=[]):
        """
        This method creates a string out of a datalist to make it appendable for the csv file writer
        From: https://appdividend.com/2020/09/24/python-list-to-string/#:~:text=To%20convert%20the%20list%20to%20string%20in%20Python%2C,iterable%2C%20separated%20by%20a%20string%20separator%20if%20provided.
        :param data: [date,account_number,balance,currency]
        :return: str (with the concatenated fields of the data list)
        """
        return ','.join(data)
