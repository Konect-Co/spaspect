import numpy as np
import json

def readConfigFile(path):
	#Santript, for you
	#Goal: Read contents of the config file and return the appropriate values
	#	values include 
	#Hint: Look into json library
	#return location, link, resolution, calibration

	#opening up json file
	with open(path,"r") as f:
		neededVars = json.load(f)

	#all the necessary variables needed   
	#location = neededVars["location"]
	#link = neededVars["link"]
	#resolution = neededVars["resolution"]
	calibration = neededVars["calibration"]
	'''verticalAngle = neededVars["calibration"]["verticalAngle"]
	cameraHeight = neededVars["calibration"]["cameraHeight"]
	calibPixelCoordinates = neededVars["calibration"]["calibPixelCoordinates"]
	calib3DCoordinates = neededVars["calibration"]["calib3DCoordinates"]'''

	#return location,link,resolution,verticalAngle,cameraHeight,calibPixelCoordinates,calib3DCoordinates
	return calibration

#print(readConfigFile('sample_config.json'))
    

def getDepthMap(image_path):
	#Ravit will do
	#Goal: Take an image and run inference to get depth map
	#https://github.com/nianticlabs/monodepth2
    return

def getBoundingBoxes(image_path):
	#Ravit will do
	#Goal: Take an image and run inference to get bounding boxes
	#https://github.com/tensorflow/models/tree/master/research/object_detection
    return

def getPixelDepth(pixel_coordinate, depth_map, pixel_radius=10):
	#Santript, for you
	#Goal: Apply the algorithm we were discussing on finding the depth
	#	take a circle of radius pixel_radius
	#	find 50% of values of depth distribution centered at the given pixel
	#	later, we'll incorporate same solution with masks
    return

def calculateCalibrationConstant(path):
	#calculating calibration information from the calibration pixel and 3D coordinates

	calibration = readConfigFile(path)

	calibPixelCoordinate = calibration["calibPixelCoordinate"]
	calib3DCoordinate = calibration["calib3DCoordinate"]

	verticalAngle = calibration["verticalAngle"]

	cameraDirection = [0, 1, -np.sin(verticalAngle)]
	cameraDirection = np.asarray(cameraDirection)

	height = calibration["cameraHeight"]
	cameraPosVector = np.asarray([0, 0, height])

	coordinate2camera  = calib3DCoordinate - cameraPosVector

	# dot product = product of magnitudes - 
	cos_angle = np.dot(cameraDirection, coordinate2camera) / (np.linalg.norm(cameraDirection) * np.linalg.norm(coordinate2camera))
	angle = np.arccos(cos_angle)

	#Santript, for you
	#Now, all that is needed is to return calib_constant
	calib_constant = np.tan(angle)/np.linalg.norm(calibPixelCoordinate)
	#but one thing to consider... tangent(angle) = tangent(arccosine(cos_angle))
	#soooo.... it is better to rewrite np.tan(angle) as math.sqrt(1-cos_angle*cos_angle)/cos_angle

	return calib_constant

def calculate3DCoordinates(pixelCoordinate, depthMap, calibrationConstant):
	#Santript, for you
	#calculating 3D coordinates given pixel coordinate and calibration information
    return

a = calculateCalibrationConstant("./sample_config.json")
print(a)
