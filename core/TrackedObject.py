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
			
			for tracked_key in cls.objects:
				tracked = cls.objects[tracked_key]
				if (currTime-tracked.getLastUpdate() > updateThreshold):
					to_delete.append(tracked_key)
			
			for delete_i in to_delete:
				del cls.objects[delete_i]
			
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

			print("[DEBUG] boundingBoxes", boundingBoxes)

			allIOUValues = {}
			for name in cls.objects.keys():
				trackedEntity = cls.objects[name]
				predictedBox = trackedEntity.computePrediction()
				IOUValues = {}
				for box_i in range(len(boundingBoxes)):
					box = boundingBoxes[box_i]

					IOU = cv_utils.computeIOU(predictedBox, box)
					IOUValues[box_i] = IOU
				IOUValues = sorted(allIOUValues.items(), reverse=True, key = lambda kv:(kv[1], kv[0]))
				allIOUValues[trackedEntity.getName()] = IOUValues
			
			print("[DEBUG] allIOUValues", allIOUValues)

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
			#storing the indices of the new boxes that are to be created
			minThresholdIOU = 0.3			
			newBoxes = []			
			while True:
				keys = allIOUValues.keys()
				if len(keys) == 0:
					break

				maximum_iou = 0
				maximumTracking = keys[0]

				for trackingObj in keys:
					#problem: val is not the global maximum just for the current tracked object
					iou = allIOUValues[trackingObj][0]
					if iou>maximum_iou:
						maximum_iou = iou
						maximumTracking = trackingObj
				
				#if the greatest iou left is lower than the minimum threshold
				#adding all remaining bounding boxes to be created as new objects
				if maximum_iou < minThresholdIOU:
					for box_i in allIOUValues[keys[0]].keys():
						newBoxes.append(box_i)
					break

				#if not, we update the latest box and repeat
				else:
					maximumTracking.addBox(allIOUValues[maximumTracking].keys()[0])
					boxKey = allIOUValues[maximumTracking].keys()[0]
					
					#deleting the row and column of the maximum IoU
					for trackingKey in allIOUValues.keys():
						   del(allIOUValues[trackingKey][boxKey])
					
					#adding remaining boxes
					for box_i in allIOUValues[maximumTracking].keys():
						newBoxes.append(box_i)
					del(allIOUValues[val])
					print("[DEBUG] \tTracked object being updated")

			#making a new object
			for newBoxIndex in newBoxes:
				name1 = str(random.random())
				label = "person"
				boundingBox = boundingBoxes[newBoxIndex]
				print("[DEBUG] \tNew object being constructed")
				newObject = TrackedObject(name1,label,boundingBox)

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
