import utils
import time

class TrackedObject(object):
	#number of seconds without detection until tracked object can be removed
	updateThreshold = 5
	#keeping track of the time
	currTime = 0
	#all objects that are being tracked
	objects = []

	def __init__(self, name, label):
		#name of the tracked object
		self.name = name
		#class for the bounding box
		self.label = label
		#pixel velocity of tracked object (pixel/second)
		self.velocity = [0, 0]
		#dictionary storing time as key and bounding box as value
		self.history = {}
		#number of seconds since last detection of object
		self.lastUpdate = 0
	
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
			
			for tracked_i in range(len(objects)):
				tracked = objects[tracked_i]
				if (currTime-tracked.getLastUpdate() > updateThreshold):
					to_delete.append(tracked_i)
			
			to_delete.sort(reverse=True)
			for delete_i in to_delete:
				del objects[delete_i]
			
			return

	@classmethod
	def addAll(cls, boundingBoxes):
			#this method is the essence of the tracking algorithm
			#it goes through the boundingBoxes in the new detection
			#and updates the tracked objects' positions through the add function
			#this should update the time stored in the class variable
			#assigned : Cassiano
			cls.updateTime()

			for (name in history.keys()):
				trackedEntity = history[name]
				predictedBox = trackedEntity.computePrediction()
				for box in boundingBoxes:
					print("Do stuff!")
					#check IoU with every bounding box
					#assign the correct bounding box as the latest box of this particular tracked object
					#Warning: Make sure though that one bounding box is not assigned to multiple tracked objects

			cls.prune()
			return

	def add(self, bounding_box):
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
