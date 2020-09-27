import math
import json

import cv_model.utils as cv_utils
import TrackedObject

###UTILS FUNCTIONS START###

"""
Finds all realtime coordinates

@params pm, CVOutput, score_threshold
@return map of X Y Z 3D coordinates and longitude/latitude coordinates
"""
def genCoordinates(pm, CVOutput, score_threshold=0.60):
	boxes = []
	X3D_vals = []
	Y3D_vals = []
	Z3D_vals = []
	lat_vals = []
	lon_vals = []

	#checking whether detection scores matches criteria and checks the object detection keys
	for i in range(len(CVOutput["boxes"])):
		if (CVOutput["scores"][i] < score_threshold):
			break
		if (not CVOutput["classes"][i] == "person"):
			continue
		
		#indices of detection boxes
		box = CVOutput["boxes"][i]

		#finding midpoint
		midpoint = [int((box[0]+box[2])/2), box[3]]

		#using conversions from PixelMapper.py
		lonlat = pm.pixel_to_lonlat(midpoint)[0]
		coord3D = pm.lonlat_to_3D(lonlat)

		boxes.append(box)
		lat_vals.append(lonlat[0])
		lon_vals.append(lonlat[1])
		X3D_vals.append(coord3D[0])
		Y3D_vals.append(coord3D[1])
		Z3D_vals.append(coord3D[2])

	allCoordinates={"boxes":boxes, "X3D_vals":X3D_vals, "Y3D_vals": Y3D_vals, "Z3D_vals": Z3D_vals, "lat_vals":lat_vals, "lon_vals": lon_vals}
	return allCoordinates



"""
Determines value representing mask wearing

@params CVOutput
@return value(0, 1, or 2) representing whether detected person is wearing mask or not
"""	
def genMaskData(CVOutput):
	#part that determines whether person is wearing mask
	#0=unsure, 1=wearing, 2=not wearing
	masked = []

	#face and mask detection
	for box in CVOutput["boxes"]:
		wearingMask = 0
		for maskOut in CVOutput["masks"]:
			face_box = maskOut[0]
			mask = maskOut[1]
			#computing IOA of face_box and box
			IOA = cv_utils.computeIOA(face_box, box)
			#setting the value of wearingMask based on IOA value
			if (IOA > 0.9):
				if (mask>0.7):
					wearingMask = 1
				else:
					wearingMask = 2
				break
		masked.append(wearingMask)

	return masked



"""
Determines whether person is distanced or not

@params coordinatesData(output of genCoordinates()), distance_threshold
@return value of 0 or 1 representing undistanced or distanced
"""
def genDistanceData(coordinatesData, distance_threshold=2):

	X3D_vals = coordinatesData["X3D_vals"]
	Y3D_vals = coordinatesData["Y3D_vals"]
	Z3D_vals = coordinatesData["Z3D_vals"]

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

"""
Generates tracking data.
"""
def genTrackingData(coordinatesData, masked, distanced):
	boxes = coordinatesData["boxes"]
	X3D_vals = coordinatesData["X3D_vals"]
	Y3D_vals = coordinatesData["Y3D_vals"]
	Z3D_vals = coordinatesData["Z3D_vals"]

	print("NEW Objects", len(X3D_vals))

	TrackedObject.TrackedObject.track(boxes, X3D_vals, Y3D_vals, Z3D_vals, masked, distanced)
	trackedObjects = TrackedObject.TrackedObject.objects
	trackedData = {id:trackedObject.toDict() for (id, trackedObject) in trackedObjects.items()}
	return trackedData

"""
Combines all the functions above to generate all realtime analytics within this one function.

@params pm, CVOutput, filename(json file where all realtime analytics will be placed), distance_threshold, score_threshold
@return all realtime analytics
"""
def genRealData(pm, CVOutput, streamLink, filename, distance_threshold=2):
	# starting point for realtime data
	realData = genCoordinates(pm, CVOutput)

	realData["streamLink"] = streamLink

	distanced = genDistanceData(realData)
	realData["distanced"] = distanced	

	masked = genMaskData(CVOutput)
	realData["masked"] = masked

	tracked = genTrackingData(realData, masked, distanced)
	realData["tracked"] = tracked

	#TODO: Add data on tracked individuals as well
	with open(filename, 'w') as f:
		json.dump(realData, f, indent=4)
	return realData