import csv

def testcsv():
    with open("UScities.csv") as csvff:
        readCSV = csv.reader(csvff, delimiter=',')
        zips=[]
        for row in readCSV:
            print(row[0])
            print(row[1])

testcsv()
