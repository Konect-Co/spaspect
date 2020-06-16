import numpy as np
import json
import math
import cv2
from depth_model import pred_depth

from torchvision import transforms, datasets

def readConfigFile(path):
	#Goal: Read contents of the config file and return the appropriate values
	#Hint: Look into json library
	with open(path,"r") as f:
		neededVars = json.load(f)

	calibration = neededVars["calibration"]
	return calibration

def getDepthMap(image_path):
	#Ravit will do
	#Goal: Take an image and run inference to get depth map
	#https://github.com/nianticlabs/monodepth2
    
    """Function to predict for a single image or folder of images
    """
    depth = pred_depth.predict(image_path)
    return depth

def getBoundingBoxes(image_path):
	#Ravit will do
	#Goal: Take an image and run inference to get bounding boxes
	#https://github.com/tensorflow/models/tree/master/research/object_detection
    return

def getPixelDepth(pixel_coordinate_x, pixel_coordinate_y, depth_map, img, pixel_radius=10):
	#Santript, for you
	#Goal: Apply the algorithm we were discussing on finding the depth
	#	take a circle of radius pixel_radius
	#	find 50% of values of depth distribution centered at the given pixel
	#	later, we'll incorporate same solution with masks
    
    allDepth = getDepthMap('test_image.jpg')
    
    img1 = cv2.imread(img,0)
    indices = np.where(img1 != [0])
    coordinates = zip(indices[0], indices[1])
    
    neededPixels = []
    for (pixel_x, pixel_y) in coordinates:
        if (pixel_x - pixel_coordinate_x)**2 + (pixel_y - pixel_coordinate_y)**2 <= (pixel_radius**2):
                neededPixels.append(pixel_x,pixel_y)
    
    allPixelDepth = []
    for pixels in neededPixels:
        allPixelDepth.append(allDepth[pixels])
    
    length = len(allPixelDepth)
    allPixelDepth.sort()
    neededLength = int(length/2)
    neededDepth = allPixelDepth[neededLength]
        
    
    return neededDepth

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
	#angle = np.arccos(cos_angle)

	#Santript, for you
	#Now, all that is needed is to return calib_constant
	calib_constant = (math.sqrt(1-cos_angle*cos_angle))/cos_angle/np.linalg.norm(calibPixelCoordinate)
	#but one thing to consider... tangent(angle) = tangent(arccosine(cos_angle))
	#soooo.... it is better to rewrite np.tan(angle) as math.sqrt(1-cos_angle*cos_angle)/cos_angle

	return calib_constant

def calculate3DCoordinates(pixelCoordinate, depthMap, calibrationConstant):
	#Santript, for you
	#calculating 3D coordinates given pixel coordinate and calibration information
    return