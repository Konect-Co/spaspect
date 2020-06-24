import os
import numpy as np
import json
import math
import sys
from vision.torchvision import transforms, datasets

import utils
from cv_model import pred

#TODO: Write this in C++ to optimize inference speed

class SpaSpectCore:
	"""
	Function that initializes the SpaSpectCore class
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

		self.calibConstant = self.calculateCalibrationConstant()

		self.image = None
		self.CVOutput = None

		self.labels = None
		self.spatialCoordinates = None
		self.pixelCoordinates = None
		self.updateImage()
		self.updatePredictions()

		#array of positions needed for pose estimation
		self.COCO_PERSON_KEYPOINT_NAMES = [
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
	def updateImage(self):
		image = utils._readImage(self.imagePath)
		self.image = image
		return image

	"""
	Runs the computer vision model on the specified image and stores the output
	"""
	def updatePredictions(self):
		output = pred.predict(self.imagePath)
		
		self.CVOutput = output
		return output

	"""
	One-time use function to calibrate the calibration constant for the given configuration
	"""
	def calculateCalibrationConstant(self):
		assert self.calibration != None and "EMPTY: calibration value is None."

		#calculating calibration information from the calibration pixel and Spatial coordinates
		calibPixelCoordinate = self.calibration["calibPixelCoordinate"]
		calibSpatialCoordinate = self.calibration["calibSpatialCoordinate"]
		verticalAngle = self.calibration["verticalAngle"]
		height = self.calibration["cameraHeight"]

		calibConstant = utils._calculateCalibrationConstant(verticalAngle, height, calibPixelCoordinate, calibSpatialCoordinate)
		self.calibConstant = calibConstant

		return calibConstant

	"""
	ASSISTANT BIG BOI FUNCTION
	Uses pixelCoordinate and calibration information to calculate a spatial coordinate
	"""
	def calculateSpatialCoordinate(self):

		#all necessary variables from calibration file
		#testing
		center = np.array(self.calibration["centerpoint"])
		#print(center)
		verticalAngle = self.calibration["verticalAngle"]
		height = self.calibration["cameraHeight"]
		depthMap = pred.predict("pics/TimesSquare.mp4")["depth"]
		pixelRadius = 10
		#print(depthMap)

		#finds the pixel coordinate of the nose of a person(nose just for now. It might change)
		
		numPeople = self.CVOutput["keypoints"].shape[0]
		#print(numPeople)
		for i in range(numPeople):
			pixelCoordinate = self.CVOutput["keypoints"][i][self.COCO_PERSON_KEYPOINT_NAMES.index("nose")][:2]
			
		#print(self.CVOutput["keypoints"].shape)
		#print(pixelCoordinate)
		#calibration constant
		k = self.calculateCalibrationConstant()
		#print(k)

		actualSpatialCoord = utils._calculateSpatialCoordinate(pixelCoordinate, center, verticalAngle, k, height, depthMap, pixelRadius)

		return actualSpatialCoord
    

	"""
	BIG BOI Function
	Uses pixelCoordinates to make the map
	"""
	def calculateSpatialMap(self):
		spatialCoordinates = []
		for pixelCoordinate in self.pixelCoordinates:
			spatialCoordinates.append(self.calculateSpatialCoordinate(pixelCoordinate))
		self.spatialCoordinates = spatialCoordinates
		return

configPath = "configs/times_square.json"
imagePath = "pics/TimesSquare.mp4"
coreExample = SpaSpectCore(configPath, imagePath)

sys.stdout = open("textfiles/3DCoords.txt","w")
print("3D Coordinates: ", coreExample.calculateSpatialCoordinate())
sys.stdout.close()