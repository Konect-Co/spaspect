import os
import csv
import time
import random

location = "TimesSquare"

#TODO: Implement this
def getNumPeople():
	return random.randint(1, 5)

#TODO: Implement this
def getAverageDistance():
	return random.randint(1, 5)

counter = 0
with open(os.path.join(os.getcwd(), "csvFiles", location) + ".csv", 'w', newline="") as f:
	writer = csv.writer(f, delimiter=",")
	writer.writerow(["time", "num_people", "average_distance"])
	while True:
		currTime = time.time()

		num_people = getNumPeople()
		average_distance = getAverageDistance()

		writer.writerow([currTime, num_people, average_distance])
	
		counter += 1
		if (counter == 5):
			break