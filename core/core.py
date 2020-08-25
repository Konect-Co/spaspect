import sys
import utils
import cv2

from cv_model import pred
import PixelMapper
import TrackedObject

import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore

# Ravit Uncomment:
cred = credentials.Certificate('/home/ravit/Downloads/spaspect-dashboard-firebase-adminsdk-bip9h-4407f5fe40.json')

# Santript Uncomment:
#cred = credentials.Certificate('/home/santript/ImportantProjects/Files/spaspect-dashboard-firebase-adminsdk-bip9h-8efff333dc.json')

firebase_admin.initialize_app(cred)

db = firestore.client()

def main(dashboard):
	dashboardDoc = db.collection(u'dashboards').document(dashboard)
	dashboardInfo = dashboardDoc.get().to_dict()

	streamLink = dashboardInfo["streamlink"]

	#streamLink = "/home/santript/ImportantProjects/Files/NewClearPeople.mp4"


	# Ravit Uncomment:
	imagePath = "/home/ravit/Pictures/Frame.jpg"
	#streamLink = "/home/ravit/Downloads/TimesSquare.mp4"

	# Santript Uncomment:
	#imagePath = "/home/santript/ImportantProjects/Frames/Frame.jpg"
	#streamLink = "/home/santript/ImportantProjects/Files/TimesSquare2.mp4"

	cap = cv2.VideoCapture()
	cap.open(streamLink)

	calibration = dashboardInfo["calibration"]
	dashboardOutput = dashboardInfo["output"]
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

		#print("predOutput:",predOutput)
		#print(predOutput["tracked"])

		        
		frame_index += 1

		dashboardOutput["X3D_vals"] = predOutput["X3D_vals"]
		dashboardOutput["Y3D_vals"] = predOutput["Y3D_vals"]
		dashboardOutput["Z3D_vals"] = predOutput["Z3D_vals"]
		dashboardOutput["lat_vals"] = predOutput["lat_vals"]
		dashboardOutput["lon_vals"] = predOutput["lon_vals"]
		dashboardOutput["masked"] = predOutput["masked"]
		dashboardOutput["distanced"] = predOutput["distanced"]
		dashboardOutput["tracked"] = predOutput["tracked"]
        
		print("New Dashboard: ",dashboardInfo)
        
		dashboardDoc.set(dashboardInfo)	

		"""
		for tracked_obj in predOutput["tracked"].values():
			id = float(tracked_obj["name"])
			color = (int((id%1)*255), int((id*100%1)*255), int((id*10000%1)*255))
			current_pos = tracked_obj["history"][str(tracked_obj["lastUpdate"])]
			current_pos = [int(elem) for elem in current_pos]
			image = cv2.rectangle(image, (current_pos[0], current_pos[1]), (current_pos[2], current_pos[3]), color, 2)
			for i in range(len(list(tracked_obj["history"]))-1):
				pos_c = tracked_obj["history"][list(tracked_obj["history"])[i]]
				pos_n = tracked_obj["history"][list(tracked_obj["history"])[i+1]]

				midpoint_c = (int((pos_c[0] + pos_c[2])/2),int((pos_c[1] + pos_c[3])/2))
				midpoint_n = (int((pos_n[0] + pos_n[2])/2),int((pos_n[1] + pos_n[3])/2))

				image = cv2.line(image, midpoint_c, midpoint_n, color, 2)
		cv2.imwrite("/home/santript/ImportantProjects/Frames/frame" + str(frame_index) + ".jpg", image)
		"""

	return 0


if __name__ == "__main__":
	dashboard = "d3c4fd41-8892-453b-bc00-64d1f494284b"
	sys.exit(main(dashboard))
