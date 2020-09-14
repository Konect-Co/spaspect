import sys
from utilScripts import readDashboard
from utilScripts import obtainStreamLink
import cv2
import RealTime

from cv_model import pred
import PixelMapper
#import TrackedObject

def main(dashboardID):
	dashboardInfo = readDashboard.read(dashboardID)

	calibration = dashboardInfo["calibration"]

	pixelX = calibration["pixelX_vals"]
	pixelY = calibration["pixelY_vals"]
	pixel_array = [[pixelX[i], pixelY[i]] for i in range(len(pixelX))]
	lat = calibration["lat_vals"]
	lon = calibration["lon_vals"]
	lonlat_array = [[lat[i], lon[i]] for i in range(len(lat))]
	pm = PixelMapper.PixelMapper(pixel_array, lonlat_array, calibration["lonlat_origin"])

	if ("streamlink" in calibration.keys()):
		streamLink = calibration["streamLink"]
	else ():
		streamLink = obtainStreamLink(calibration["streamWebpage"])

	cap = cv2.VideoCapture()
	cap.open(streamLink)

	frame_rate = cv2.CAP_PROP_FPS
	frame_index = 0

	while True:
		print("FRAME", frame_index, "##############")
		
		read, image = cap.read()
		if (not read):
			print("END")
			break

		# generating prediction from image
		output = pred.predict(image)

		RealTime.genRealData(pm, output)
		Aggregate.genAggData()

		frame_index += 1

	return 0

if __name__ == "__main__":
	dashboardID = "d3c4fd41-8892-453b-bc00-64d1f494284b"
	sys.exit(main(dashboardID))
