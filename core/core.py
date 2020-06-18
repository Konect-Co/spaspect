import os
import numpy as np
import json
import math
import cv2
from torchvision import transforms, datasets

from cv_model import pred

#TODO: Write this in C++ to optimize inference speed

class SpaSpectCore:
	"""
	function that initializes the SpaSpectCore class
	"""
	def __init__(self, configPath, imagePath):
		assert os.path.exists(configPath), "ERROR: specified configPath does not exist."
		self.configPath = configPath

		assert os.path.exists(imagePath), "ERROR: specified imagePath does not exist."
		self.imagePath = imagePath

		with open(configPath,"r") as f:
			configInfo = json.load(f)

		self.location = configInfo["location"]
		self.calibration = configInfo["calibration"]
		self.resolution = configInfo["resolution"]

		self.calib_constant = calculateCalibrationConstant()

		self.image = None
		self.cv_output = None
		self.map3D = None
		self.pixelCoordinates = None

		#array of positions needed for pose estimation
		COCO_PERSON_KEYPOINT_NAMES = [
			'nose',
			'left_eye',
			'right_eye',
			'left_ear',
			'right_ear',
			'left_shoulder',
			'right_shoulder',
			'left_elbow',
			'right_elbow',
			'left_wrist',
			'right_wrist',
			'left_hip',
			'right_hip',
			'left_knee',
			'right_knee',
			'left_ankle',
			'right_ankle'
		]

		COCO_INSTANCE_CATEGORY_NAMES = [
			'__background__', 'person', 'bicycle', 'car', 'motorcycle', 'airplane', 'bus',
			'train', 'truck', 'boat', 'traffic light', 'fire hydrant', 'N/A', 'stop sign',
			'parking meter', 'bench', 'bird', 'cat', 'dog', 'horse', 'sheep', 'cow',
			'elephant', 'bear', 'zebra', 'giraffe', 'N/A', 'backpack', 'umbrella', 'N/A', 'N/A',
			'handbag', 'tie', 'suitcase', 'frisbee', 'skis', 'snowboard', 'sports ball',
			'kite', 'baseball bat', 'baseball glove', 'skateboard', 'surfboard', 'tennis racket',
			'bottle', 'N/A', 'wine glass', 'cup', 'fork', 'knife', 'spoon', 'bowl',
			'banana', 'apple', 'sandwich', 'orange', 'broccoli', 'carrot', 'hot dog', 'pizza',
			'donut', 'cake', 'chair', 'couch', 'potted plant', 'bed', 'N/A', 'dining table',
			'N/A', 'N/A', 'toilet', 'N/A', 'tv', 'laptop', 'mouse', 'remote', 'keyboard', 'cell phone',
			'microwave', 'oven', 'toaster', 'sink', 'refrigerator', 'N/A', 'book',
			'clock', 'vase', 'scissors', 'teddy bear', 'hair drier', 'toothbrush'
		]

	"""
	Function that is responsible for updating the image by reading it from imagePath
	"""
	def updateImage():
		self.image = cv2.imread(self.image_path)

	"""
	One-time use function to calibrate the calibration constant for the given configuration
	"""
	def calculateCalibrationConstant():
		assert self.calibration != None && "EMPTY: calibration value is None."

		#calculating calibration information from the calibration pixel and 3D coordinates
		calibPixelCoordinate = self.calibration["calibPixelCoordinate"]
		calib3DCoordinate = self.calibration["calib3DCoordinate"]

		verticalAngle = self.calibration["verticalAngle"]

		cameraDirection = [0, 1, -np.sin(verticalAngle)]
		cameraDirection = np.asarray(cameraDirection)

		height = self.calibration["cameraHeight"]
		cameraPosVector = np.asarray([0, 0, height])

		coordinate2camera  = calib3DCoordinate - cameraPosVector

		# dot product = product of magnitudes - 
		cos_angle = np.dot(cameraDirection, coordinate2camera) / (np.linalg.norm(cameraDirection) * np.linalg.norm(coordinate2camera))
		#angle = np.arccos(cos_angle)

		#one thing to consider... tangent(angle) = tangent(arccosine(cos_angle))
		#soooo.... it is better to rewrite np.tan(angle) as math.sqrt(1-cos_angle*cos_angle)/cos_angle
		calib_constant = (math.sqrt(1-cos_angle*cos_angle)/cos_angle)/np.linalg.norm(calibPixelCoordinate)
		self.calib_constant = calib_constant

		return calib_constant

	"""
	runs the computer vision model on the specified image and stores the output
	"""
	def runCVModel():
		#Goal: Take an image and run inference to get depth map and bounding boxes
		#https://github.com/nianticlabs/monodepth2
		#Pytorch computer vision model

		#TODO: Update predict function so it processes self.image instead of reading from self.imagePath
		depth, output = pred.predict(self.imagePath)
		
		#TODO: Find a better representation
		output["depth"] = depth
		self.cv_output = output

		return depth, output

	"""
	Uses pixelCoordinate to obtain the depth
	"""
	def getPixelDepth(pixelCoordinate, pixel_radius=10):
		#Goal: Apply the algorithm we were discussing on finding the depth
		#	take a circle of radius pixel_radius
		#	find 50% of values of depth distribution centered at the given pixel
		#	later, we'll incorporate same solution with masks

		pixelCoordinateX = pixelCoordinate[0]
		pixelCoordinateY = pixelCoordinate[1]

		#finds all the pixel coordinates of an image
		indices = np.where(self.image != [0])
		coordinates = zip(indices[0], indices[1])

		#extracts all the pixels that are within a 10 pixel radius from the center pixel coordinate
		neededPixels = []
		for (pixelX, pixelY) in coordinates:
			if (pixelX - pixelCoordinateX)**2 + (pixelY - pixelCoordinateY)**2 <= (pixel_radius**2):
				    neededPixels.append(pixelX,pixelY)
				    
		#gets the depth of neededPixels using depth estimation
		pixelDepths = []
		for pixels in neededPixels:
			pixelDepths.append(self.depthMap[pixels])
			
		#finds the final needed depth
		length = len(pixelDepths)
		pixelDepths.sort()
		neededLength = int(length/2)
		neededDepth = pixelDepths[neededLength]
		
		return neededDepth

	"""
	ASSISTANT BIG BOI FUNCTION
	Uses pixelCoordinate to calculate a 3D coordinate
	"""
	def calculate3DCoordinate(pixelCoordinate):
		#calculating 3D coordinates given pixel coordinate and calibration information

		with open("sample_config.json","r") as f:
			neededVars = json.load(f)

		#all necessary variables from json file
		center = neededVars["calibration"]["centerpoint"]
		v = neededVars["calibration"]["verticalAngle"]
		height = neededVars["calibration"]["cameraHeight"]

		#finds the pixel coordinate of the nose of a person(nose just for now. It might change)
		pixelCoordinate = self.output["keypoints"][:][COCO_PERSON_KEYPOINT_NAMES.index("nose")]

		#finds the offset of object from center of image(distance)
		offset = pixelCoordinate-center

		#calibration constant
		k = calculateCalibrationConstant("sample_config.json")

		#needed to find the camera direction vector(how much camera has to move to have a direct view of object)
		delta_x = k * math.atan(offset[0])
		delta_y = k * math.atan(offset[1])

		#3D direction vector
		directionVector = [math.tan(delta_x), 1, math.tan(delta_y - v)]

		#finds the magnitude of the 3D direction vector(needed for normalization)
		magnitude = math.sqrt(directionVector[0]**2 + directionVector[1]**2 + directionVector[2]**2)

		#uses magnitude to normalize the 3D direction vector
		normalized = directionVector/magnitude

		#finds depth of pixelCoordinate using the getPixelDepth function(needed to find the actual 3D coordinates of object)
		depth = getPixelDepth(pixelCoordinate)

		#camera's 3D coordinates IRL
		camera_position = [0,0,height]

		#3D coordinates of object
		actual3DCoords = depth * normalized + camera_position

		return actual3DCoords

	"""
	BIG BOI Function
	Obtains the relevant pixelCoordinates
	pixelCoordinates is a list where each element is [<object_label>, <3D_coordinate>]
	"""
	def makePixelCoordinates():
		#This function will make pixelCoordinates and variable and add it to self.pixelCoordinates
		return

	"""
	BIG BOI Function
	Uses pixelCoordinates to make the map
	"""
	def calculate3DMap():
		map3D = []
		for pixelCoordinate in self.pixelCoordinates:
			map3D.append([ pixelCoordinate[0], calculate3DCoordinate(pixelCoordinate[1]) ])
		self.map3D = map3D
	
	"""
	MEGA BOI Function
	responsible for the full flow from image + calibration file --> 3D map
	"""
	def makeMap():
		#BIG BOI Function #1: obtain relevant pixelCoordinates
		makePixelCoordinates

		#BIG BOI Function #2: use pixelCoordinates to make the map
		calculate3DMap()
