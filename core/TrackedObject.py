class TrackedObject(object):
	def __init__(self, name, label):
		#name of the tracked object
		self.name = name
		#class for the bounding box
		self.label = label
		#pixel velocity of tracked object (pixel/second)
		self.velocity = velocity
		#dictionary storing time as key and bounding box as value
		self.history = {}
		#number of seconds since last detection of object
		self.lastUpdate = 0
		
		#number of seconds without detection until tracked object can be removed
		updateThreshold = 5
		#keeping track of the time (TODO: incorporate with python time library)
		time = 0
		#all objects that are being tracked storing name as key and object as value
		objects = {}

	#TODO: Add getter functions for all of the instance/class variables

	@classmethod
	def updateTime():
		#TODO
		#Updates the class time variable when called

	@classmethod
	def prune(cls):
		#remove all tracked objects which have not been updated within updateThreshold seconds
		#TODO
		return

	@classmethod
	def addAll(cls, boundingBoxes):
		#this method is the essence of the tracking algorithm
		#it goes through the boundingBoxes in the new detection
		#and updates the tracked objects' positions through the add function
		#this should update the time stored in the class variable
		#TODO

	def add(self, time, bounding_box):
		history[time] = bounding_box
		return

	def updateVelocity(self):
		#given that there are at least two bounding boxes in history
		#calculate the pixel velocity

		velocity = 0
		#TODO: Implement this method
		self.velocity = velocity
		return
