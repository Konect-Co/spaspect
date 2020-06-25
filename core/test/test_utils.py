import csv
import utils
import ast

def test_add():
    with open("testcases/add_tests.csv") as csv_file:
        reader = csv.reader(csv_file, delimiter=",")
        first = True
        for row in reader:
            if first:
                first = False
                continue
            a = int(row[0])
            b = int(row[1])
            expected = int(row[2])
            assert utils._add(a, b) == expected
			
def test_calculateCalibrationConstant():
	with open("testcases/calibrationConstant_tests.csv") as csv_file:
		reader = csv.reader(csv_file, delimiter=";")
		first = True
		for row in reader:
			if first:
				first = False
				continue
			a = float(row[0])
			b = float(row[1])
			c = ast.literal_eval(row[2].strip())
			d = ast.literal_eval(row[3].strip())
			expected = float(row[4])
			print(a)
			assert utils._calculateCalibrationConstant(a,b,c,d) == expected