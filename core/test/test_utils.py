import utils
import csv

def test_add():
    with open("add_tests.csv") as csv_file:
        reader = csv.reader(csv_file, delimiter=",")
        first = True
        for row in reader:
            if first:
                first = False
                continue
            a = int(row[0])
            b = int(row[1])
            expected = int(row[2])
            assert utils.add(a, b) == expected