from Phemex.JournalWriter.writer import Writer

#TODO: CLASS CAN BE REMOVED AFTER TESTING
if __name__ == '__main__':
    list = ['06.02.2022,9232830001,0.03567667,BTC', 'abcde']
    teststring = '06.02.2022'

    for i in range(0, len(list)):
        print(teststring in list[i])
