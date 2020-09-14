import numpy as np
import math
import os
import json
import cv_model.utils as cv_utils
#import TrackedObject

#TODO: Place these utils functions into a new file
###UTILS FUNCTIONS START###
def genCoordinates(pm, CVOutput, score_threshold=0.60):
	X3D_vals = []
	Y3D_vals = []
	Z3D_vals = []
	lat_vals = []
	lon_vals = []

	boxes = []

	#checking whether detection scores matches criteria and checks the object detection keys
	for i in range(len(CVOutput["detection_boxes"])):
		if (CVOutput["detection_scores"][i] < score_threshold):
			break
		if (not CVOutput["detection_classes"][i] == "person"):
			continue
		
		#indices of detection boxes
		box = CVOutput["detection_boxes"][i]
		boxes.append(box)

		#finding midpoint
		midpoint = [int((box[0]+box[2])/2), box[3]]

		#using conversions from PixelMapper.py
		long_lat = pm.pixel_to_lonlat(midpoint)[0]
		coord3D = pm.lonlat_to_3D(long_lat)


		lat_vals.append(long_lat[0])
		lon_vals.append(long_lat[1])
		X3D_vals.append(coord3D[0])
		Y3D_vals.append(coord3D[1])
		Z3D_vals.append(coord3D[2])

	allCoordinates={"X3D_vals":X3D_vals, "Y3D_vals": Y3D_vals, "Z3D_vals": Z3D_vals, "lat_vals":lat_vals, "lon_vals": lon_vals}
	return allCoordinates
	# have json write this dictionary to file

def genMaskData(CVOutput):
	#part that determines whether person is wearing mask
	#0=unsure, 1=wearing, 2=not wearing
	masked = []

	wearingMask = 0
	faceBoxes_subList = []
	boxes_subList = []
	#face and mask detection
	for maskOut in CVOutput["masks"]:
		face_box = maskOut[0]
		mask = maskOut[1]
		faceBoxes_subList.append(face_box)
		boxes_subList.append(box)
		#computing IOA of face_box and box
		IOA = cv_utils.computeIOA(face_box, box)
		#setting the value of wearingMask based on IOA value
		if (IOA > 0.9):
			if (mask>0.7):
				wearingMask = 1
			elif (mask < 0.7):
				wearingMask = 2
			else:
				break
	masked.append(wearingMask)

	return masked

def genDistanceData(pm, CVOutput, distance_threshold=2):
	#determines whether person is distanced or not

	X3D_vals = genCoordinates(pm, CVOutput)["X3D_vals"]

	distanced = [1] * len(X3D_vals)
	for i in range(len(X3D_vals)):
		for j in range(i+1, len(X3D_vals)):
			if (distanced[i] == 0 and distanced[j] == 0):
				continue
			#setting distance to 0 for not distanced and 1 for distanced
			distance = [X3D_vals[i]-X3D_vals[j], Y3D_vals[i]-Y3D_vals[j], Z3D_vals[i]-Z3D_vals[j]]
			distance = math.sqrt(sum([element**2 for element in distance]))
			#makes sure that distance is not above 1
			if (distance < distance_threshold):
				distanced[i] = 0
				distanced[j] = 0
		if 1 not in distanced:
			break
	return distanced
###UTILS FUNCTIONS END###

#returns a map of all the realtime analytics
def genRealData(pm, CVOutput, distance_threshold=2, score_threshold=0.60):
	# starting point for realtim data
	realData = genCoordinates(pm, CVOutput)

	masked = genMaskData(CVOutput)
	distanced = genDistanceData(pm, CVOutput)

	realData["masked"] = masked
	realData["distanced"] = distanced
	#TODO: Add data on tracked individuals as well

	return realData