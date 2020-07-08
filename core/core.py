import json
import time
import math
import os
import sys
import utils
import numpy as np
import cv2

import PixelMapper
import TrackedObject
from cv_model import pred
import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore

# Use a service account
cred = credentials.Certificate('/home/santript/ImportantProjects/Files/spaspect-dashboard-firebase-adminsdk-bip9h-73fbdcc01a.json')
firebase_admin.initialize_app(cred)

root_dir = "/home/santript/ImportantProjects/spaspect/visualization"
db = firestore.client()

def main(dashboard):
	dashboardDoc = db.collection(u'dashboards').document(dashboard)
	dashboardInfo = dashboardDoc.get().to_dict()
	#with open("/home/ravit/Konect-Code/spaspect-project/spaspect/visualization/output/0443639c-bfc1-11ea-b3de-0242ac130004.json", "r") as f:
	#	dashboardInfo = json.loads(f.read())

	imagePath = "/home/santript/ImportantProjects/Frames/Frame.jpg"
	streamLink = dashboardInfo["streamlink"]
	streamLink = "/home/santript/ImportantProjects/Files/TimesSquare2.mp4"

	cap = cv2.VideoCapture()
	cap.open(streamLink)

	calibration = dashboardInfo["calibration"]
	pixelX = calibration["pixelX_vals"]
	pixelY = calibration["pixelY_vals"]
	pixel_array = [[pixelX[i], pixelY[i]] for i in range(len(pixelX))]
	lat = calibration["lat_vals"]
	lon = calibration["lon_vals"]
	lonlat_array = [[lat[i], lon[i]] for i in range(len(lat))]
	pm = PixelMapper.PixelMapper(pixel_array, lonlat_array, calibration["lonlat_origin"])

	video = False
	frame_rate = cv2.CAP_PROP_FPS
	frame_index = 0

	for _ in range(10):
		cap.read()

	while True:
		print("FRAME", frame_index, "##############")
		
		read, image = cap.read()
		if (not read):
			print("END")
			break

		cv2.imwrite(imagePath, image)
		output = pred.predict(imagePath)

		predOutput = utils.makeVisualizationOutput(pm, output)
		print(predOutput["trackedObjects"])
        
		frame_index += 1
		
		dashboardInfo["output"] = predOutput
		
		dashboardDoc.set(dashboardInfo)
		
		#break
		
		"""
		startTime = time.time()
		interval = int(time.time()-startTime)
		if (interval<5):
			time.sleep(5-interval)
			interval = 5
		if (video):
			for _ in range(interval*frame_rate):
				cap.read()"""

	return 0


root_path = "/home/santript/ImportantProjects/spaspect"
if __name__ == "__main__":
	args = {
		"imagePath":"/home/santript/ImportantProjects/Frames/Frame.jpg",
		"dashboard":"",
		"configPath":"/home/santript/ImportantProjects/spaspect/visualization/config/TimesSquare.json",
		"isVideo":True
	}
	dashboard = "0443639c-bfc1-11ea-b3de-0242ac130004"
	sys.exit(main(dashboard))