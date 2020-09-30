import csv
import os


def getAverageDist(location):
	with open(os.path.join(os.getcwd(), "csvFiles", location) + ".csv", 'r') as csv_file:
		reader = csv.DictReader(csv_file)
		data = [row for row in reader]
		

getAverageDist("Dublin")