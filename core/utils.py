import numpy as np
import math
import cv_model.utils as cv_utils

def makeVisualizationOutput(pm, output, distance_threshold=2, score_threshold = 0.80):
	coords3D = []
	long_lats = []
	wearingMasks = []
	faceBoxes = []
	boxes = []
	for i in range(len(output["boxes"])):
		#print("Boxes", output["boxes"][i])
		if (output["scores"][i] < score_threshold):
			break
		box = output["boxes"][i]
		
		midpoint = [int((box[0]+box[2])/2), box[3]]

		long_lat = pm.pixel_to_lonlat(midpoint)[0]
		coord3D = pm.lonlat_to_3D(long_lat)

		#0=unsure, 1=wearing, 2=not wearing
		wearingMask = 0
		#print(output["masks"])
		faceBoxes_subList = []
		boxes_subList = []
		for maskOut in output["masks"]:
			face_box = maskOut[0]
			mask = maskOut[1]
			#print("boxA: ",face_box)
			#print("boxB: ",box)
			faceBoxes_subList.append(face_box)
			boxes_subList.append(box)
			IOA = cv_utils.computeIOA(face_box, box)
			#print("IOA: ", IOA)
			if (IOA > 0.9):
				if (mask>0.7):
					wearingMask = 1
				elif (mask < 0.7):
					wearingMask = 2
				else:
					wearingMask = 0
				break

		long_lats.append(long_lat)
		coords3D.append(coord3D)
		wearingMasks.append(wearingMask)
		faceBoxes.append(np.array(faceBoxes_subList).tolist())
		boxes.append(np.array(boxes_subList).tolist())

	if (coords3D != []):
		long_lats = np.swapaxes(np.asarray(long_lats), 0, 1).tolist()
		coords3D = np.asarray(coords3D).tolist()
	if (faceBoxes != []):
		faceBoxes = np.asarray(faceBoxes).tolist()
	if (boxes != []):
		boxes = np.asarray(boxes).tolist()

	safe = [1] * len(coords3D)
	for i in range(len(coords3D)):
		for j in range(i+1, len(coords3D)):
			if (safe[i] == 0 and safe[j] == 0):
				continue
			assert len(coords3D[i]) == len(coords3D[j])
			distance = math.sqrt(sum(e**2 for e in [coords3D[i][k]-coords3D[j][k] for k in range(2)]))
			if (distance < distance_threshold):
				safe[i] = 0
				safe[j] = 0
	#print("faceBoxes:", faceBoxes)
	#print("boxes:", boxes)
	predOutput = {"3DCoordinates":coords3D, "lat-long":long_lats,"Boxes":boxes, "Faces":faceBoxes, "wearingMasks":wearingMasks, "safe":safe}
	return predOutput
