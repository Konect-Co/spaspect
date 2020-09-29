# Copyright 2020 The Konect SpaSpect Authors. All Rights Reserved.
# This file is part of Konect SpaSpect technology.
#  ___            ___              _   
# / __|_ __  __ _/ __|_ __  ___ __| |_ 
# \__ \ '_ \/ _` \__ \ '_ \/ -_) _|  _|
# |___/ .__/\__,_|___/ .__/\___\__|\__|
#     |_|            |_|               


from cv_model import pred

from utilScripts import readDashboard
from utilScripts import obtainStreamLink
from utilScripts import RealTime
from utilScripts import Aggregate
from utilScripts import PixelMapper

import sys
import cv2
import os
import time

#file where realtime and aggregate will be
fbFilesDir = os.path.join(os.path.dirname(os.getcwd()), "firebaseFiles")

"""
Determines the realtime and aggregate analytics frame by frame of a video stream

@params dashboardID(firebase document ID)
@return 0 if executed successfully
"""
def main(dashboardID):
	# Getting all dashboard data in dictionary format
	dashboardInfo = readDashboard.read(dashboardID)

	#calibration information from firebase files
	calibration = dashboardInfo["calibration"]

	pixelX = calibration["pixelX_vals"]
	pixelY = calibration["pixelY_vals"]
	#getting pixel coordinates from pixelX and pixelY
	pixel_array = [[pixelX[i], pixelY[i]] for i in range(len(pixelX))]

	lat = calibration["lat_vals"]
	lon = calibration["lon_vals"]

	#getting longitude and latitude coordinates from lat and lon
	lonlat_array = [[lat[i], lon[i]] for i in range(len(lat))]
	
	# Obtaining pixelMapper object from calibration information
	pm = PixelMapper.PixelMapper(pixel_array, lonlat_array, calibration["lonlat_origin"])

	# Obtaining streamLink (statically or dynamically) from calibration
	# either "streamLink" or "streamWebpage" should be present in calibration
	streamLinkStatic = calibration["static"]
	streamLink = None
	
	#getting streamlink from calibration json file
	#sets the value of streamLinkStatic
	if ("streamLink" in calibration.keys()):
		streamLink = calibration["streamLink"]
		streamLinkStatic = True
	if (not streamLinkStatic):
		assert "streamWebpage" in calibration.keys()

	# For debug purposes

	#streamLinkStatic = True
	#streamLink = "https://video2archives.earthcam.com/archives/_definst_/MP4:network/9974/2020/09/22/1500.mp4/playlist.m3u8"

	# Opening the videoCApture object
	cap = cv2.VideoCapture()

	frame_index = 0

	startTime = time.time()

	video = False
	if (video):
		fps = 50
	while True:
		frame_index += 1

		# TODO: Refreshing every second may not be the best approach
		# if the streamLink is not static, then it's necessary to continuously refresh
		if (streamLinkStatic and frame_index == 1):
			cap.open(streamLink)
		if (not streamLinkStatic):
			streamLink = obtainStreamLink.get(calibration["streamWebpage"])
			cap.open(streamLink)

		read, image = cap.read()
		if (not read):
			print("Frame", frame_index, "not read.")
			continue

		if (video):
			if (frame_index%(fps*1) != 0):
				continue

		print("FRAME", frame_index, "##############")

		# generating prediction from image
		output = pred.predict(image)


		#generates the realtime and aggregate analytics displayed on spaspect dashboard
		realData = RealTime.genRealData(pm, output, streamLink, os.path.join(fbFilesDir, "realtime") + os.path.sep + dashboardID + ".json")
		aggData = Aggregate.genAggData(realData, os.path.join(fbFilesDir, "aggregate") + os.path.sep + dashboardID + ".json")

		if (video):
			delayTime = (frame_index*1.0/fps)-(time.time()-startTime)
			if (delayTime>0):
				time.sleep(delayTime)

	return 0


"""
Setting sample dashboard ID for parameter
"""
if __name__ == "__main__":
	#TIMES SQUARE
	dashboardID = "0443639c-bfc1-11ea-b3de-0242ac130004"
	#DUBLIN
	#dashboardID = "1ff9e8ae-bfc1-11ea-b3de-0242ac130004"
	#SOUTHLAKE
	#dashboardID = "9f5a8845-4c78-4da3-b76e-bbc8c76eacc0"
	sys.exit(main(dashboardID))
