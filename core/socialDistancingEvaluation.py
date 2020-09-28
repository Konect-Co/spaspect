import cv2
from cv_model import pred

from utilScripts import obtainStreamLink
from utilScripts import PixelMapper
from RealTimeAnalytics import RealTime

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
def getAverageDistance(pm, CVOutput):
	real_time = RealTime.genRealData(pm, CVOutput);
	X3D_vals = real_time["X3D_vals"];
	y3D_vals = real_time["Y3D_vals"];
	Z3D_vals = real_time["Z3D_vals"];

	for i in range(len(X3D_vals)):
		for j in range(i+1, len(X3D_vals)):
			distance = [X3D_vals[i]-X3D_vals[j], Y3D_vals[i]-Y3D_vals[j], Z3D_vals[i]-Z3D_vals[j]]
			distance = math.sqrt(sum([element**2 for element in distance]))
	totalDist = 0
	for dist in distance:
		totalDist += dist
		avgDist = totalDist / len(distance)

	return avgDist

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