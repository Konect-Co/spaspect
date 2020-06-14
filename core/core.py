import numpy as np

def readConfigFile (path):
	#Santript, for you
	#Goal: Read contents of the config file and return the appropriate values
	#	values include 
	#Hint: Look into json library
	#return location, link, resolution, calibration
	

def getDepthMap (image_path):
	#Ravit will do
	#Goal: Take an image and run inference to get depth map
	#https://github.com/nianticlabs/monodepth2

def getBoundingBoxes (image_path):
	#Ravit will do
	#Goal: Take an image and run inference to get bounding boxes
	#https://github.com/tensorflow/models/tree/master/research/object_detection

def getPixelDepth (pixel_coordinate, depth_map, pixel_radius=10):
	#Santript, for you
	#Goal: Apply the algorithm we were discussing on finding the depth
	#	take a circle of radius pixel_radius
	#	find 50% of values of depth distribution centered at the given pixel
	#	later, we'll incorporate same solution with masks

def calculateCalibrationConstant (calibPixelCoordinate, calib3DCoordinate):
	#Santript, for you
	#calculating calibration information from the calibration pixel and 3D coordinates

def calculate3DCoordinates (pixelCoordinate, depthMap, calibrationConstant):
	#Santript, for you
	#calculating 3D coordinates given pixel coordinate and calibration information
