import utils
import cv_model.utils as cv_utils
import time
import random

#TODO: objects variable varies from configuration to configuration. Therefore
	# it should be separately instantiated rather than kept in the same class.
class TrackedObject(object):
	#number of seconds without detection until tracked object can be removed
	updateThreshold = 5
	#keeping track of the time
	currTime = 0
	#all objects that are being tracked
	objects = {}

	def __init__(self, name, label, boundingBox, X3D, Y3D, Z3D):

		#name of the tracked object
		self.name = name
		#class for the bounding box
		self.label = label
		#pixel velocity of tracked object (pixel/second)
		self.velocity = [0, 0]
		#dictionary storing time as key and bounding box as value
		self.history = {}
		#number of seconds since last detection of object
		self.lastUpdate = type(self).currTime
		#adding box
		self.addBox(boundingBox, X3D, Y3D, Z3D)
		#adding self to objects
		assert name not in type(self).objects.keys()
		type(self).objects[name] = self

	def toDict(self):
		return {
			"name":self.name,
			"label":self.label,
			"velocity":self.velocity,
			"history":self.history,
			"lastUpdate":self.lastUpdate
		}

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
	def getHistoryKeys(self):
		return list(self.history.keys())

	@classmethod
	def updateTime(cls):
			#assigned : Santript
			#Updates the class time variable when called
			cls.currTime = time.time()
			return

	@classmethod
	def prune(cls):
			#remove all tracked objects which have not been updated within updateThreshold seconds
			to_delete = []

			for tracked_key in cls.objects:
				tracked = cls.objects[tracked_key]
				if (cls.currTime-tracked.getLastUpdate() > cls.updateThreshold):
					to_delete.append(tracked_key)

			for delete_i in to_delete:
				del cls.objects[delete_i]

			return

	@classmethod
	def track(cls, boundingBoxes, X3D_values, Y3D_values, Z3D_values):
			#this method is the essence of the tracking algorithm
			#it goes through the boundingBoxes in the new detection
			#and updates the tracked objects' positions through the add function
			#this should update the time stored in the class variable
			#assigned : Santript

			#TODO: (for future) Make algorithm more efficient by implementing grids in the image
			#TODO: Consider edge case where the same object alternates between two tracking objects
			cls.updateTime()

			allIOUValues = {}
			for name in cls.objects.keys():
				trackedEntity = cls.objects[name]
				predictedBox = trackedEntity.computePrediction()
				IOUValues = {}
				for box_i in range(len(boundingBoxes)):
					box = boundingBoxes[box_i]

					#BUG: Returning negative values, sometimes values over 1
					IOU = cv_utils.computeIOU(predictedBox, box)
					
					IOUValues[box_i] = IOU


				#print("IOU: ", IOUValues)
			    #print("IOU: ", allIOUValues)

				IOUValues = {k : v for k, v in sorted(IOUValues.items(), reverse=True, key = lambda kv:kv[1])}
				allIOUValues[trackedEntity] = IOUValues
                
				#print("Items: ",allIOUValues.items())
				#fprint("Name: ",trackedEntity.getName())

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
			if len(allIOUValues.keys()) == 0:
				newBoxes = range(len(boundingBoxes))
			else:
				while True:
					#keys = allIOUValues.keys()
					keys = list(allIOUValues)
					if len(keys) == 0:
						break
					if len(allIOUValues[keys[0]]) == 0:
						break

					maximum_iou = 0
					maximumTracking = keys[0]

					for trackingObj in keys:
						iou = allIOUValues[trackingObj][list(allIOUValues[trackingObj])[0]]
						if iou>maximum_iou:
							maximum_iou = iou
							maximumTracking = trackingObj


					#if the greatest iou left is lower than the minimum threshold
					#adding all remaining bounding boxes to be created as new objects
					if maximum_iou < minThresholdIOU:
						for box_i in list(allIOUValues[keys[0]].keys()):
							newBoxes.append(box_i)
						break

					#if not, we update the latest box and repeat
					else:
						boxKey = list(allIOUValues[maximumTracking])[0]
						maximumTracking.addBox(
							boundingBoxes[boxKey], X3D_values[boxKey], Y3D_values[boxKey], Z3D_values[boxKey]
						)

						#deleting the row and column of the maximum IoU
						for trackingKey in list(allIOUValues):
							del(allIOUValues[trackingKey][boxKey])

						del(allIOUValues[maximumTracking])

            #making a new object
			for newBoxIndex in newBoxes:
				name1 = str(random.random())
				label = "person"
				boundingBox = boundingBoxes[newBoxIndex]
				#print("PAUSE")
				newObject = TrackedObject(name1,label,boundingBox, X3D_values, Y3D_values, Z3D_values)
			cls.prune()
			return
			

	def addBox(self, bounding_box, X_3D, Y_3D, Z_3D):
		#assigned : Ravit
		if len(self.history.keys()) != 0:
			assert self.lastUpdate != type(self).currTime
		self.history[str(type(self).currTime)] = {"bounding_box": bounding_box.tolist(), "X3D": X_3D, "Y3D": Y_3D, "Z3D": Z_3D}
		self.lastUpdate = type(self).currTime
		self.updateVelocity()
		#print("History keys1: ", self.history.keys()[-1])
		#print("History keys2: ", self.history.keys()[-2])
		return

	def updateVelocity(self):
		#assigned : Richard
		#given that there are at least two bounding boxes in history
		#calculate the pixel velocity
		#velocity = difference in position(in pixels)/difference in time(time between each frame)
		
		if len(self.history.keys()) < 2:
			self.velocity = [0, 0]
			return
        
		time_i = list(self.history.keys())[-1]
		time_f = list(self.history.keys())[-2]

		bounding_box_i = self.history[time_i]['bounding_box'] #initial position
		bounding_box_f = self.history[time_f]['bounding_box'] #final position

		xVelocity = (bounding_box_f[0] - bounding_box_i[0])/(float(time_f) - float(time_i))
		yVelocity = (bounding_box_f[1] - bounding_box_i[1])/(float(time_f) - float(time_i))

		velocity = [xVelocity, yVelocity]
		self.velocity = velocity
		return

	def computePrediction(self):
		if len(self.history.keys()) != 0:
			assert self.lastUpdate != type(self).currTime
		delta_t = type(self).currTime - self.lastUpdate

		velocity = self.getVelocity()
		history = self.getHistory()
		lastPosition = history[list(history.keys())[-1]]['bounding_box']
		predictedPosition = [0] * len(lastPosition) #should be [0, 0]

		#if the velocity is 0, return the current box as is
		if (velocity == 0):
			return lastPosition
        
		#print("Last position: ",lastPosition)
		#print("Length of last position: ",len(lastPosition))
		assert len(lastPosition) == 4
		assert len(velocity) == 2
		for coord_i in range(len(lastPosition)):
			currComponent = lastPosition[coord_i]
			currComponent += velocity[coord_i%2]*delta_t
			predictedPosition[coord_i] = currComponent
		return predictedPosition
