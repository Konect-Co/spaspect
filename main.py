import sys
import math
import json
import time

"""
TODO:
- rewrite js drawer to take into account the new format of points.json
- fix errors in pixel-->aerial: right now it is returning negative y coordinates (which shouldn't even be possible 🤔️)

"""

from GenPixCoordinates import makePeopleCoordinates
from utils import *

#TODO: Add support for multiple calibration points
#TODO: Add support for rotated frame
#TODO: Pay attention to exceptions related to inverse trig functions
#TODO: Ensure there is no radian/degree mismatch
#TODO: Finish pixel2aerial function

#converts horizontalAngle and verticalAngle to a normalized direction vector
def angle2direction(horizontalAngle, verticalAngle):
	y = 1
	x = math.sin(horizontalAngle)
	z = math.sin(verticalAngle)

	directionVector = [x, y, z]
	directionVector = normalize(directionVector)

	return directionVector

#converts a direction vector to horizontalAngle and verticalAngle
def direction2angle(directionVector):
	x = directionVector[0]
	y = directionVector[1]
	z = directionVector[2]

	#TODO: Instead of printing "ERROR", throw an error
	if (y == 0):
		print("ERROR: y cannot be 0 in the direction vector")
	
	factor = 1/y #we want y to be 1
	directionVector = scale(directionVector, factor)

	horizontalAngle = math.asin(x)
	verticalAngle = math.asin(z)

	return horizontalAngle, verticalAngle

#calculating k: the fixed ratio defined as tan(angle)/length, where angle is the angle from the and length is the distance from the pixel coordinates to the center of the screen which aligns with camera direction
def calcK(height, cameraDirection, calibPixelCoordinates, calibAerialCoordinates):
	#finding angle between camera direction vector and vector (calibAerialCoordinates-cameraPosition)
	angle = findAngle(cameraDirection, add(calibAerialCoordinates, [0, 0, -height]))
	pixelLength = length(calibPixelCoordinates)
	k = math.tan(angle)/pixelLength
	return k

#pixelCoordinates to aerialCoordinates given calibration information
def pixel2aerial (pixelCoordinates, height, cameraDirection, k):
	centerCoordinate = [0, 0]

	negCenter = []
	for c in centerCoordinate:
		negCenter.append(-c)

	coordinates = []
	for pixelCoordinate in pixelCoordinates:
		pixelCoordinate = add(pixelCoordinate, negCenter)
		#pixelLength = length(pixelCoordinate)

		cameraVerticalAngle, cameraHorizontalAngle = direction2angle(cameraDirection)

		verticalDelta = math.atan(k*pixelCoordinate[0])
		horizontalDelta = math.atan(k*pixelCoordinate[1])

		lineVerticalAngle = cameraVerticalAngle + verticalDelta
		lineHorizontalAngle = cameraHorizontalAngle + horizontalDelta

		lineDirection = angle2direction(lineHorizontalAngle, lineVerticalAngle)
		
		coordinates.append(findIntersection(height, lineDirection)[:2])
	return coordinates



def makeCoordinates(image_url, height, cameraDirection, calibPixelCoordinates, calibAerialCoordinates):
	pixelCoordinates = makePeopleCoordinates(image_url)

	#TODO: Think, is it reasonable for pixel coordinates to be [10, 10] but aerial coordinates to be [0, 100] for example?
	#It seems that there should be some criteria that constrain the possible values for the aerial coordinates, no?
	k = calcK(height, cameraDirection, calibPixelCoordinates, calibAerialCoordinates)

	coordinates = pixel2aerial(pixelCoordinates, height, cameraDirection, k)
	return coordinates

#while True:
print("Refreshing coordinates")

start_time = time.time()
end_time = start_time + 5

with open('webapp/points.json', 'r') as json_file:
	data = json.load(json_file)

	for location in data.keys():
			data_current = data[location][0]
			
			image_url = data_current["image_url"]
			height = data_current["height"]
			cameraDirection = data_current["cameraDirection"]
			calibPixelCoordinates = data_current["calibPixelCoordinates"]
			calibAerialCoordinates = data_current["calibAerialCoordinates"]

			coordinates = makeCoordinates(image_url, height, cameraDirection, calibPixelCoordinates, calibAerialCoordinates)
			

			data[location][0]["coordinates"] = coordinates
			print(coordinates)

	#with open('webapp/points.json', 'w') as json_file:
		#json.dump(data, json_file, indent="\t")
	
	#Takes ~50 ms to run one iteration of inference and file read/write on AMD GPU

	#if (remaining_time > 0):
		#time.sleep(remaining_time)
