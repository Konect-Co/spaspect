import csv
import ast
import sys
sys.path.insert(0, r'C:\Users\Cassiano\Desktop\spaspect\core')
import utils
import numpy as np
from numpy import load

def test_add():
    with open(r"C:\Users\Cassiano\Desktop\spaspect\core\testcases\add_tests.csv") as csv_file:
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
	with open(r"C:\Users\Cassiano\Desktop\spaspect\core\testcases\calibrationConstant_tests.csv") as csv_file:
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

def test_getPixelDepth():
	with open(r"C:\Users\Cassiano\Desktop\spaspect\core\testcases\getPixelDepth_tests.csv") as csv_file:
		reader = csv.reader(csv_file, delimiter=';')
		npy_reader = load(r"C:\Users\Cassiano\Desktop\spaspect\core\testcases\depth.npy")
		first = True
		for row in reader:
			if first:
				first = False
				continue
			a = ast.literal_eval(row[0].strip())
			b = npy_reader
			c = float(row[1])
			expected = float(row[2])
			assert np.allclose(utils._getPixelDepth(a,b,c),expected)

def test_calculateSpatialCoordinate():
	#pixelCoordinate, center, verticalAngle, k, height, depthMap, pixelRadius
	with open(r"C:\Users\Cassiano\Desktop\spaspect\core\testcases\calculateSpatialCoordinate_tests.csv") as csv_file:
		reader = csv.reader(csv_file, delimiter=';')
		npy_reader = load(r"C:\Users\Cassiano\Desktop\spaspect\core\testcases\depth.npy")
		first = True
		for row in reader:
			if first:
				first = False
				continue
			a = ast.literal_eval(row[0].strip())	#pixelCoordinate
			b = float(row[1])						#center					
			c = float(row[2])						#verticalAngle
			d = float(row[3])						#k
			e = float(row[4])						#height
			f = float(row[5])						#pixelRadius
			depthMap = npy_reader
			expected = ast.literal_eval(row[6].strip())
			assert np.allclose(utils._calculateSpatialCoordinate(a,b,c,d,e,depthMap,f),expected)