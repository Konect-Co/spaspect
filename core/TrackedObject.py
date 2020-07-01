import utils
import cv_model.utils as cv_utils
import time
import random

class TrackedObject(object):
	#number of seconds without detection until tracked object can be removed
	updateThreshold = 5
	#keeping track of the time
	currTime = 0
	#all objects that are being tracked
	objects = {}

	def __init__(self, name, label, boundingBox):
		
		#name of the tracked object
		self.name = name
		#class for the bounding box
		self.label = label
		#pixel velocity of tracked object (pixel/second)
		self.velocity = [0, 0]
		#dictionary storing time as key and bounding box as value
		self.history = {}
		#number of seconds since last detection of object
		self.lastUpdate = currTime
		#adding box
		self.addBox(boundingBox)
		#adding self to objects
		assert name not in objects.keys()
		objects[name] = self
	
	def getName(self):
		return self.name

	def getLabel(self):
		return self.label

	def getVelocity(self):
		return self.velocity

	def getHistory(self):
		return self.history

	def getLastUpdate(self):
		return self.lastUpdate

	@classmethod
	def updateTime(cls):
			#assigned : Santript
			#Updates the class time variable when called
			currTime = time.time()
			return

	@classmethod		
	def prune(cls):
			#remove all tracked objects which have not been updated within updateThreshold seconds
			to_delete = []
			
			for tracked_key in objects:
				tracked = objects[tracked_key]
				if (currTime-tracked.getLastUpdate() > updateThreshold):
					to_delete.append(tracked_key)
			
			for delete_i in to_delete:
				del objects[delete_i]
			
			return

	@classmethod
	def track(cls, boundingBoxes):
			#this method is the essence of the tracking algorithm
			#it goes through the boundingBoxes in the new detection
			#and updates the tracked objects' positions through the add function
			#this should update the time stored in the class variable
			#assigned : Santript

			#TODO: (for future) Make algorithm more efficient by implementing grids in the image
			cls.updateTime()

			allIOUValues = {}
			for name in objects.keys():
				trackedEntity = objects[name]
				predictedBox = trackedEntity.computePrediction()
				IOUValues = {}
				for box_i in range(len(boundingBoxes)):
					box = boundingBoxes[box_i]

					IOU = cv_utils.computeIOU(predictedBox, box)
					IOUValues[box_i] = IOU
				IOUValues = sorted(allIOUValues.items(), reverse=True, key = lambda kv:(kv[1], kv[0]))
				allIOUValues[trackedEntity.getName()] = IOUValues
				
			keys = allIOUValues.keys()
			for val in keys:
				maximum_iou = allIOUValues[val][0]
				minIOU = 0.3
				if maximum_iou < minIOU:
					name1 = str(random.random())
					label = "person"
					boundingBox = boundingBoxes[allIOUValues[val].keys()[0]]
					newObject = TrackedObject(name1,label,boundingBox)
					return
				else:
					val.addBox(allIOUValues[val].keys()[0])
					key = allIOUValues[val].keys()[0]
					del(allIOUValues[val])
					for trackingKey in allIOUValues.keys():
						   del(allIOUValues[trackingKey][key])

			"""
			Now, we have a 2D dictionary with the row corresponding to each existing tracked object
			and each column corresponding to each bounding box.
			Here's the procedure for updating the bounding boxes of tracked entities
			- Start with the highest IoU currently in the 2D dictionary
			- If the highest IoU is lower than the threshold IoU, then
				- take all existing bounding boxes and assign them to new tracking objects
				- return
			- Otherwise
				- Assign the bounding box corresponding to the highest IoU to the corresponding tracking object
			- Delete the row and column of the highest IOU from the 2D dictionary
			"""

			cls.prune()
			return

	def addBox(self, bounding_box):
		#assigned : Ravit
		assert self.lastUpdate != currTime		

		history[currTime] = bounding_box
		self.lastUpdate = currTime
		return

	def updateVelocity(self):
		#assigned : Richard
		#given that there are at least two bounding boxes in history
		#calculate the pixel velocity
		#velocity = difference in position(in pixels)/difference in time(time between each frame)
		if len(self.history) < 2:
			self.velocity = [0, 0]
			return

		time_i = self.history.keys()[-1]
		time_f = self.history.keys()[-2]

		bounding_box_i = self.history[time_i] #initial position
		bounding_box_f = self.history[time_f] #final position
		
		xVelocity = (bounding_box_f[0] - bounding_box_i[0])/(time_f - time_i)
		yVelocity = (bounding_box_f[1] - bounding_box_i[1])/(time_f - time_i)
		
		velocity = [xVelocity, yVelocity]
		self.velocity = velocity
		return

	def computePrediction(self):
		assert self.lastUpdate != currTime
		delta_t = currTime - self.lastUpdate

		velocity = self.getVelocity()
		history = self.getHistory()
		lastPosition = history[hisotry.keys()[-1]]
		predictedPosition = [0] * len(lastPosition) #should be [0, 0]

		#if the velocity is 0, return the current box as is
		if (velocity == 0):
			return lastPosition

		for coord_i in range(len(lastPosition)):
			coord = lastPosition[coord_i]
			assert len(coord) == len()
			for component_i in range(len(coord)):
				currComponent = coord[component_i]
				currComponent += velocity[component_i]*delta_t
				predictedPosition[coord_i][component_i] = currComponent
		
		return currentPosition				
