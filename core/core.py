import sys
from utilScripts import readDashboard
from utilScripts import obtainStreamLink
import cv2
import RealTime

from cv_model import pred
import PixelMapper
#import TrackedObject

fbFilesDir = os.path.join(os.path.dirname(os.getcwd()), "firebaseFiles")

def main(dashboardID):
	# Getting all dashboard data in dictionary format
	dashboardInfo = readDashboard.read(dashboardID)

	calibration = dashboardInfo["calibration"]

	pixelX = calibration["pixelX_vals"]
	pixelY = calibration["pixelY_vals"]
	pixel_array = [[pixelX[i], pixelY[i]] for i in range(len(pixelX))]
	lat = calibration["lat_vals"]
	lon = calibration["lon_vals"]
	lonlat_array = [[lat[i], lon[i]] for i in range(len(lat))]
	
	# Obtaining pixelMapper object from calibration information
	pm = PixelMapper.PixelMapper(pixel_array, lonlat_array, calibration["lonlat_origin"])

	# Obtaining streamLink (statically or dynamically) from calibration
	# either "streamLink" or "streamWebpage" should be present in calibration
	# 
	streamLinkStatic = False
	streamLink = None
	if ("streamLink" in calibration.keys()):
		streamLink = calibration["streamLink"]
		streamLinkStatic = True
	else:
		assert "streamWebpage" in calibration.keys()
		streamLinkStatic = False

	# Opening the videoCApture object
	cap = cv2.VideoCapture()
	cap.open(streamLink)

	frame_index = 0

	while True:
		print("FRAME", frame_index, "##############")
		
		# TODO: Refreshing every second may not be the best approach
		# if the streamLink is not static, then it's necessary to continuously refresh
		if (not streamLinkStatic):
			streamLink = obtainStreamLink(calibration["streamWebpage"])

		read, image = cap.read()
		if (not read):
			print("END")
			break

		# generating prediction from image
		output = pred.predict(image)

		RealTime.genRealData(pm, output, os.path.join(fbFilesDir, "realtime"))
		Aggregate.genAggData(os.path.join(fbFilesDir, "aggregate"))

		frame_index += 1

	return 0

if __name__ == "__main__":
	dashboardID = "d3c4fd41-8892-453b-bc00-64d1f494284b"
	sys.exit(main(dashboardID))
