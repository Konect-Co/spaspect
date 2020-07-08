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
cred = credentials.Certificate('/home/ravit/Downloads/spaspect-dashboard-firebase-adminsdk-bip9h-4407f5fe40.json')
firebase_admin.initialize_app(cred)

root_dir = "/home/ravit/Konect-Code/spaspect-project/spaspect/visualization"
db = firestore.client()

class Dashboard(object):
	def __init__(self, name, streamlink, calibration, output):
		self.name = name
		self.streamlink = streamlink
		self.calibration = calibration
		self.output = output

	@staticmethod
	def from_dict(source):
		result = Dashboard(source["name"], source["streamlink"], source["calibration"], source["output"])
		return result

	def to_dict(self):
		result = {
			u"name":self.name.decode(),
			u"streamlink":self.streamlink.decode(),
			u"calibration":self.calibration,
			u"output":self.output
		}
		return output

	def __repr__ (self):
		return(
			f'Dashboard(\
				name={self.name}, \
				streamlink={self.streamlink}, \
				calibration={self.calibration}, \
				output={self.output}, \
			)'
		)


def main(dashboard):
	dashboardDoc = db.collection(u'dashboards').document(dashboard)
	dashboardInfo = dashboardDoc.get().to_dict()
	#with open("/home/ravit/Konect-Code/spaspect-project/spaspect/visualization/output/0443639c-bfc1-11ea-b3de-0242ac130004.json", "r") as f:
	#	dashboardInfo = json.loads(f.read())

	imagePath = "/home/ravit/Konect-Code/Frame.jpg"
	streamLink = dashboardInfo["streamlink"]
	streamLink = "/home/ravit/Downloads/TimesSquare2.mp4"

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


root_path = "/home/ravit/Konect-Code/spaspect-project/spaspect"
if __name__ == "__main__":
	args = {
		"imagePath":"/home/ravit/Pictures/Frame.jpg",
		"dashboard":"",
		"configPath":"/home/ravit/Konect-Code/spaspect-project/spaspect/visualization/config/TimesSquare.json",
		"isVideo":True
	}
	dashboard = "0443639c-bfc1-11ea-b3de-0242ac130004"
	sys.exit(main(dashboard))