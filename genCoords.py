import sys
import math
import utils

#TODO: Add support for multiple calibration points
#TODO: Add support for rotated frame
#TODO: Pay attention to exceptions related to inverse trig functions
#TODO: Finish pixel2aerial function
#TODO: Ensure there is no radian/degree mismatch

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
	factor = 1/directionVector[1] #we want y to be 1
	directionVector = scale(directionVector, factor)

	horizontalAngle = math.asin(x)
	verticalAngle = math.asin(z)

	return horizontalAngle, verticalAngle

#pixelCoordinates to aerialCoordinates given calibration information
def pixel2aerial (pixelCoordinates, height, cameraDirection, k):
	#@Ravit will implement
	centerCoordinate = [0, 0]

	negCenter = []
	for c in centerCoordinate:
		negCenter += -c

	coordinates = []
	for pixelCoordinate in pixelCoordinates:
		pixelCoordinate = add(pixelCoordinate, negCenter)
		pixelLength = length(pixelCoordinate)

		cameraVerticalAngle, cameraHorizontalAngle = direction2angle(cameraDirection)

		verticalDelta = math.atan(k*pixelCoordinates[1])
		horizontalDelta = math.atan(k*pixelCoordinates[2])

		lineVerticalAngle = cameraVerticalAngle + verticalDelta
		lineHorizontalAngle = cameraHorizontalAngle + horizontalAngle

		lineDirection = angle2direction(lineHorizontalAngle, lineVerticalAngle)
		
		coordinates += findIntersection(height, lineDirection)
	return coordinates

#calculating k: the fixed ratio defined as tan(angle)/length, where angle is the angle from the and length is the distance from the pixel coordinates to the center of the screen which aligns with camera direction
def calcK(cameraDirection, calibPixelCoordinates, calibAerialCoordinates):
	#finding angle between camera direction vector and vector (calibAerialCoordinates-cameraPosition)
	angle = findAngle(cameraDirection, add(calibAerialCoordinates, [0, 0, -height]))
	pixelLength = length(calibPixelCoordinates)
	k = math.tan(angle)/pixelLength
	return k

def makeCoordinates(image_url):
	#@Santript Step 1: Load image_url into numpy array using cv2

	#@Santript Step 2: Run the image through object detection to get the output bounding boxes for people only

	#@Santript Step 3: For each bounding box, get the pixel coordinate of the midpoint of the bottom edge of the box and store it in pixelCoordinates

	coordinates = pixel2aerial(pixelCoordinates, sys.argv[1], sys.argv[2], sys.argv[3], sys.argv[4])
	return coordinates

coordinates = makeCoordinates(sys.argv[0])
print(coordinates)
