import numpy as np
import json
import math
<<<<<<< HEAD
import cv2
from depth_model import pred_depth
=======
from cv_model import pred
>>>>>>> 279476bb3717c72f5d1a422291b8b74f68900f11

from torchvision import transforms, datasets

def readConfigFile(path):
	#Goal: Read contents of the config file and return the appropriate values
	#Hint: Look into json library
	with open(path,"r") as f:
		neededVars = json.load(f)

	calibration = neededVars["calibration"]
	return calibration

def runCVModel(image_path):
	#Ravit will do
	#Goal: Take an image and run inference to get depth map and bounding boxes
	#https://github.com/nianticlabs/monodepth2
	#Pytorch computer vision model
    
    """Function to predict for a single image or folder of images
    """
    depth, boxes_output = pred.predict(image_path)
    return depth, boxes_output

<<<<<<< HEAD
def getBoundingBoxes(image_path):
	#Ravit will do
	#Goal: Take an image and run inference to get bounding boxes
	#https://github.com/tensorflow/models/tree/master/research/object_detection
    return

def getPixelDepth(pixel_coordinate_x, pixel_coordinate_y, img, pixel_radius=10):
=======
def getPixelDepth(pixel_coordinate_x, pixel_coordinate_y, depth_map, img, pixel_radius=10):
>>>>>>> 279476bb3717c72f5d1a422291b8b74f68900f11
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

def calculate3DCoordinates(depthMap, pixelCoordinate):
	#Santript, for you
	#calculating 3D coordinates given pixel coordinate and calibration information
    
    """top_pixel_depth = getPixelDepth(topPixelCoordinate_x, topPixelCoordinate_y, "test_image.jpg", pixel_radius=10)
    bottom_pixel_depth = getPixelDepth(bottomPixelCoordinate_x, bottomPixelCoordinate_y, "test_image.jpg", pixel_radius=10)
    
    #Θ = acos(A · B) --> dot product
    vert_theta = math.acos(top_pixel_depth * bottom_pixel_depth)
    
    z_coordinate = top_pixel_depth * math.sin(vert_theta)
    
    camera_height = neededVars["calibration"]["cameraHeight"]
    bottom_hypotenuse = math.sqrt(top_pixel_depth**2 - camera_height**2)
    """
    
    with open(json_path,"r") as f:
		neededVars = json.load(f)
    
    center = neededVars["calibration"]["centerpoint"]

	
    
    
    
    
    return