import cv2
from cv_model import pred

from utilScripts import obtainStreamLink
from utilScripts import PixelMapper
from utilScripts import RealTime
from utilScripts import readDashboard

import os
import csv
import time
import random
import math

locations = []

"""
dashboardID = "1ff9e8ae-bfc1-11ea-b3de-0242ac130004"
dashboardInfo = readDashboard.read(dashboardID)
calibration = dashboardInfo["calibration"]
pixelX = calibration["pixelX_vals"]
pixelY = calibration["pixelY_vals"]
#getting pixel coordinates from pixelX and pixelY
pixel_array = [[pixelX[i], pixelY[i]] for i in range(len(pixelX))]
lat = calibration["lat_vals"]
lon = calibration["lon_vals"]
#getting longitude and latitude coordinates from lat and lon
lonlat_array = [[lat[i], lon[i]] for i in range(len(lat))]
# Obtaining pixelMapper object from calibration information
pm = PixelMapper.PixelMapper(pixel_array, lonlat_array, calibration["lonlat_origin"])
locations.append({
"location": calibration["name"],
"streamWebpage": calibration["streamWebpage"],
"dashboardID": dashboardID,
# Getting all dashboard data in dictionary format
"dashboardInfo": dashboardInfo,
#calibration information from firebase files
"calibration": dashboardInfo["calibration"],
"pm": pm
})

dashboardID = "0443639c-bfc1-11ea-b3de-0242ac130004"
dashboardInfo = readDashboard.read(dashboardID)
calibration = dashboardInfo["calibration"]
pixelX = calibration["pixelX_vals"]
pixelY = calibration["pixelY_vals"]
#getting pixel coordinates from pixelX and pixelY
pixel_array = [[pixelX[i], pixelY[i]] for i in range(len(pixelX))]
lat = calibration["lat_vals"]
lon = calibration["lon_vals"]
#getting longitude and latitude coordinates from lat and lon
lonlat_array = [[lat[i], lon[i]] for i in range(len(lat))]
# Obtaining pixelMapper object from calibration information
pm = PixelMapper.PixelMapper(pixel_array, lonlat_array, calibration["lonlat_origin"])
locations.append({
"location": calibration["name"],
"streamWebpage": calibration["streamWebpage"],
"dashboardID": dashboardID,
# Getting all dashboard data in dictionary format
"dashboardInfo": dashboardInfo,
#calibration information from firebase files
"calibration": dashboardInfo["calibration"],
"pm": pm
})

"""

dashboardID = "12853b51-f36b-407f-b08d-cc53b92b0393"
dashboardInfo = readDashboard.read(dashboardID)
calibration = dashboardInfo["calibration"]
pixelX = calibration["pixelX_vals"]
pixelY = calibration["pixelY_vals"]
#getting pixel coordinates from pixelX and pixelY
pixel_array = [[pixelX[i], pixelY[i]] for i in range(len(pixelX))]
lat = calibration["lat_vals"]
lon = calibration["lon_vals"]
#getting longitude and latitude coordinates from lat and lon
lonlat_array = [[lat[i], lon[i]] for i in range(len(lat))]
# Obtaining pixelMapper object from calibration information
pm = PixelMapper.PixelMapper(pixel_array, lonlat_array, calibration["lonlat_origin"])
locations.append({
"location": calibration["name"],
"streamWebpage": calibration["streamWebpage"],
"dashboardID": dashboardID,
# Getting all dashboard data in dictionary format
"dashboardInfo": dashboardInfo,
#calibration information from firebase files
"calibration": dashboardInfo["calibration"],
"pm": pm
})

cap = cv2.VideoCapture()

def getCVOutput(streamLink):
	cap.open(streamLink)
	read, image = cap.read()
	if not read:
		return None
	
	CVOutput = pred.predict(image)
	return CVOutput

def getNumPeople(real_time):
	return len(real_time["X3D_vals"])

#TODO: Implement this
def getAverageDistance(real_time, streamLink):
	def distance(v1, v2):
		distance = [v2[0]-v1[0], v2[1]-v1[1], v2[2]-v1[2]]
		distance = math.sqrt(sum([element**2 for element in distance]))
		return distance

	X3D = real_time["X3D_vals"]
	Y3D = real_time["Y3D_vals"]
	Z3D = real_time["Z3D_vals"]

	#list of closest distances
	distances = []
	for i in range(len(X3D)):
		baseIndex = i+1 if i+1<len(X3D) else i-1
		closestDistance = distance([X3D[i], Y3D[i], Z3D[i]], [X3D[baseIndex], Y3D[baseIndex], Z3D[baseIndex]])
		for j in range(0, len(X3D)):
			if (i==j):
				continue
			currDistance = distance([X3D[i], Y3D[i], Z3D[i]], [X3D[j], Y3D[j], Z3D[j]])
			if (currDistance<closestDistance):
				closestDistance = currDistance
		distances.append(closestDistance)

	
	return str(distances)

counter = 0

while True:
	currTime = time.time()
	for location in locations:
		with open(os.path.join(os.getcwd(), "csvFiles", location["location"]) + ".csv", 'w', newline="") as f:
			writer = csv.writer(f, delimiter=",")
			writer.writerow(["time", "num_people", "distance_dist"])
		
			streamLink = obtainStreamLink.get(location["streamWebpage"])
			CVOutput = getCVOutput(streamLink)

			if (CVOutput is None):
				continue

			print("FRAME", counter, "LOCATION", location["location"], "MINUTE", counter/4)

			real_time = RealTime.genRealData(location["pm"], CVOutput, streamLink, None, write=False)

			num_people = getNumPeople(real_time)
			average_distance = getAverageDistance(real_time, streamLink)

			writer.writerow([currTime, num_people, average_distance])
	
		time.sleep(15-(time.time()-currTime))
		counter += 1
		if (counter == 4*60):
			break