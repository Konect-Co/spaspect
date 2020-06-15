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
    location = neededVars["location"]
    link = neededVars["link"]
    resolution = neededVars["resolution"]
    calibration = neededVars["calibration"]
    
    return location,link,resolution,calibration

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

def calculateCalibrationConstant(calibPixelCoordinate, calib3DCoordinate):
	#Santript, for you
	#calculating calibration information from the calibration pixel and 3D coordinates
    return

def calculate3DCoordinates(pixelCoordinate, depthMap, calibrationConstant):
	#Santript, for you
	#calculating 3D coordinates given pixel coordinate and calibration information
    return
