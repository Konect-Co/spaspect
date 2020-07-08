import numpy as np
import math
import cv_model.utils as cv_utils

def makeVisualizationOutput(pm, CVOutput, distance_threshold=2, score_threshold=0.80):
	X3D_vals = []
	Y3D_vals = []
	Z3D_vals = []
	lat_vals = []
	lon_vals = []

	masked = []
	for i in range(len(CVOutput["boxes"])):
		if (CVOutput["scores"][i] < score_threshold):
			break
		box = CVOutput["boxes"][i]
		
		midpoint = [int((box[0]+box[2])/2), box[3]]

		long_lat = pm.pixel_to_lonlat(midpoint)[0]
		coord3D = pm.lonlat_to_3D(long_lat)

		#0=unsure, 1=wearing, 2=not wearing
		wearingMask = 0
		for maskOut in CVOutput["masks"]:
			face_box = maskOut[0]
			mask = maskOut[1]
			faceBoxes_subList.append(face_box)
			boxes_subList.append(box)
			IOA = cv_utils.computeIOA(face_box, box)
			if (IOA > 0.9):
				if (mask>0.7):
					wearingMask = 1
				elif (mask < 0.7):
					wearingMask = 2
				else:
					break

		lat_vals.append(long_lat[0])
		lon_vals.append(long_lat[1])
		X3D_vals.append(coord3D[0])
		Y3D_vals.append(coord3D[1])
		Z3D_vals.append(coord3D[2])
		masked.append(wearingMask)

	distanced = [1] * len(X3D_vals)
	for i in range(len(X3D_vals)):
		for j in range(i+1, len(X3D_vals)):
			if (distanced[i] == 0 and distanced[j] == 0):
				continue
			distance = [X3D_vals[i]-X3D_vals[j], Y3D_vals[i]-Y3D_vals[j], Z3D_vals[i]-Z3D_vals[j]]
			distance = math.sqrt(sum([element**2 for element in distance]))
			if (distance < distance_threshold):
				distanced[i] = 0
				distanced[j] = 0
		if 1 not in distanced:
			break
	predOutput = {"X3D_vals":X3D_vals, "Y3D_vals":Y3D_vals, "Z3D_vals":Z3D_vals, "lat_vals":lat_vals, "lon_vals":lon_vals, "masked":masked, "distanced":distanced}
	return predOutput