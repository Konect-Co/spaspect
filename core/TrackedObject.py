import utils

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
		#assigned : Santript
		#TODO
		#Updates the class time variable when called
		return

@classmethod		
def prune(cls):
		#remove all tracked objects which have not been updated within updateThreshold seconds
		#TODO
		#assigned : Santript
		return

@classmethod
def addAll(cls, boundingBoxes):
		#this method is the essence of the tracking algorithm
		#it goes through the boundingBoxes in the new detection
		#and updates the tracked objects' positions through the add function
		#this should update the time stored in the class variable
		#TODO
		#assigned : Cassiano
		return

def add(self, time, bounding_box):
		#assigned : Ravit
		history[time] = bounding_box
		return

def updateVelocity(self, time_i, time_f):
		#assigned : Richard
		#given that there are at least two bounding boxes in history
		#calculate the pixel velocity
		#velocity = difference in position(in pixels)/difference in time(time between each frame)
		
		bounding_box_i = self.history[time_i] #initial position
		bounding_box_f = self.history[time_f] #final position
		
		xVelocity = (bounding_box_f[0] - bounding_box_i[0])/(time_f - time_i)
		yVelocity = (bounding_box_f[1] - bounding_box_i[1])/(time_f - time_i)
		velocity = [xVelocity, yVelocity]
		self.velocity = velocity
		return