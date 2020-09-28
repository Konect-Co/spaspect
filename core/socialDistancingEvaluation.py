import cv2
from cv_model import pred

from utilScripts import obtainStreamLink
from utilScripts import PixelMapper

import os
import csv
import time
import random

location = "TimesSquare"
streamWebpage = "https://www.earthcam.com/usa/newyork/timessquare/?cam=tsstreet"
cap = cv2.VideoCapture()

def getCVOutput():
	streamLink = obtainStreamLink.get(streamWebpage)
	
	cap.open(streamLink)
	read, image = cap.read()
	if not read:
		return None
	
	CVOutput = pred.predict(image)
	return CVOutput

def getNumPeople(CVOutput):
	return len(CVOutput["boxes"])

#TODO: Implement this
def getAverageDistance(CVOutput):
	return random.randint(1, 5)

counter = 0
with open(os.path.join(os.getcwd(), "csvFiles", location) + ".csv", 'w', newline="") as f:
	writer = csv.writer(f, delimiter=",")
	writer.writerow(["time", "num_people", "average_distance"])
	while True:
		currTime = time.time()

		CVOutput = getCVOutput()

		num_people = getNumPeople(CVOutput)
		average_distance = getAverageDistance()

		writer.writerow([currTime, num_people, average_distance])
	
		counter += 1
		if (counter == 5):
			break