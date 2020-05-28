import sys
import math
import json
import time

from GenPixCoordinates import makePeopleCoordinates
from utils import *

#TODO: Add support for multiple calibration points
#TODO: Add support for rotated frame

#converts horizontalAngle and verticalAngle to a normalized direction vector
def angle2direction(horizontalAngle, verticalAngle):
	x = math.tan(horizontalAngle)
	y = 1
	z = -math.tan(verticalAngle)

	directionVector = [x, y, z]
	directionVector = normalize(directionVector)

	return directionVector

#converts a direction vector to horizontalAngle and verticalAngle
def direction2angle(directionVector):
	y = directionVector[1]

	assert y == 0

	factor = 1/y #we want y to be 1
	directionVector = scale(directionVector, factor)

	x = directionVector[0]
	y = directionVector[1]
	z = directionVector[2]

	horizontalAngle = math.atan(x)
	verticalAngle = math.atan(-z)

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
	print("input pixel coordinates:", pixelCoordinates)
	print("camera height:", height)
	print("camera direction:", cameraDirection)
	print("calibration constant:", k)

	centerCoordinate = [0, 0]
	negCenter = scale(centerCoordinate, -1)

	#Note: cameraHorizontalAngle is always 0, as cameraDirection x is always 0
	cameraHorizontalAngle, cameraVerticalAngle = direction2angle(cameraDirection)
	
	print("camera vertical angle:", cameraVerticalAngle)
	print("camera horizontal angle:", cameraHorizontalAngle)

	coordinates = []
	for pixelCoordinate in pixelCoordinates:
		pixelCoordinate = add(pixelCoordinate, negCenter)
		#pixelLength = length(pixelCoordinate)

		verticalDelta = math.atan(k*pixelCoordinate[1])
		horizontalDelta = math.atan(k*pixelCoordinate[0])

		lineVerticalAngle = cameraVerticalAngle + verticalDelta
		lineHorizontalAngle = cameraHorizontalAngle + horizontalDelta

		print("vertical delta:", verticalDelta)
		print("horizontal delta:", horizontalDelta)
		print("line vertical angle:", lineVerticalAngle)
		print("line horizontal angle:", lineHorizontalAngle)

		lineDirection = angle2direction(lineHorizontalAngle, lineVerticalAngle)

		print("line direction:", lineDirection)
		
		#Assume LinePoint is [0,0,height] as it is the location of the camera
		LinePoint = [0, 0, height]
		
		#Assume PlanePoint is [0,0,0] and PlaneDirection is [0, 0, 1]
		#PlaneDirection means the vector normal to the plane
		PlanePoint = [0, 0, 0]
		PlaneDirection = [0, 0, 1]

		coordinates.append(findIntersection(LinePoint, LineDirection, PlanePoint, PlaneDirection))
	return coordinates

def makeCoordinates(image_url, height, cameraDirection, calibPixelCoordinates, calibAerialCoordinates):
	pixelCoordinates = makePeopleCoordinates(image_url)

	#TODO: Think, is it reasonable for pixel coordinates to be [10, 10] but aerial coordinates to be [0, 100] for example?
	#It seems that there should be some criteria that constrain the possible values for the aerial coordinates, no?
	k = calcK(height, cameraDirection, calibPixelCoordinates, calibAerialCoordinates)

	coordinates = pixel2aerial(pixelCoordinates, height, cameraDirection, k)
	return coordinates

height = 10
cameraDirection = [0,1,0]
calibPixelCoordinates = [0,-20]
calibAerialCoordinates = [0,10,0]

k = calcK(height, cameraDirection, calibPixelCoordinates, calibAerialCoordinates)
#print(pixel2aerial([[1, -5]], height, cameraDirection, k))

while True:
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

		with open('webapp/points.json', 'w') as json_file:
			json.dump(data, json_file, indent="\t")
		
		#Takes ~50 ms to run one iteration of inference and file read/write on AMD GPU
		remaining_time = end_time-time.time()
		if (remaining_time > 0):
			time.sleep(remaining_time)

"""

	"Location1": [
		{
			"image_url": "./CamPics/Location1.jpg",
			"height": 16,
			"cameraDirection": [
				0.0,
				1.0,
				-0.64
			],
			"calibPixelCoordinates": [
				-0.12,
				0.88
			],
			"calibAerialCoordinates": [
				0,
				16,
				0
			],
			"coordinates": [
				[
					-12.30405079729701,
					-16.00003767242668
				],
				[
					12.303939394981484,
					16.00017265596559
				]
			]
		}
	],

"""
