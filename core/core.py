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
#personalized json files for firebase
cred = credentials.Certificate('/home/ravit/Downloads/spaspect-dashboard-firebase-adminsdk-bip9h-4407f5fe40.json')

# Santript Uncomment:
#cred = credentials.Certificate('/home/santript/ImportantProjects/Files/spaspect-dashboard-firebase-adminsdk-bip9h-8efff333dc.json')

#allowing access to firebase database
firebase_admin.initialize_app(cred)

db = firestore.client()


"""
Displays all the realtime analytics on SpaSpect dashboard
"""
def main(dashboard):
	#accessing firebase dashboard and a few elements
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

	#pulls up stream from camera
	cap = cv2.VideoCapture()
	cap.open(streamLink)

	#accessing calibration information
	calibration = dashboardInfo["calibration"]
	dashboardOutput = dashboardInfo["output"]
	pixelX = calibration["pixelX_vals"]
	pixelY = calibration["pixelY_vals"]
	#getting pixel coordinates from pixelX and pixelY
	pixel_array = [[pixelX[i], pixelY[i]] for i in range(len(pixelX))]
	lat = calibration["lat_vals"]
	lon = calibration["lon_vals"]
	#getting longitude and latitude coordinates from lat and lon
	lonlat_array = [[lat[i], lon[i]] for i in range(len(lat))]

	#makes pixel, lonlat, and 3D conversions
	pm = PixelMapper.PixelMapper(pixel_array, lonlat_array, calibration["lonlat_origin"])

	video = False
	#gives the frames per second
	frame_rate = cv2.CAP_PROP_FPS
	frame_index = 0

	#reading the frames of the stream
	for _ in range(10):
		cap.read()

	while True:
		print("FRAME", frame_index, "##############")
		
		read, image = cap.read()
		if (not read):
			print("END")
			break

		#returns whether frames were successfully saved
		cv2.imwrite(imagePath, image)
		#runs object detection and mask detection
		output = pred.predict(imagePath)

		#calculates all the realtime analytics displayed on dashboard
		predOutput = utils.makeVisualizationOutput(pm, output)

		#print("predOutput:",predOutput)
		#print(predOutput["tracked"])

		        
		frame_index += 1

		#sets the output on firebase database to the output of the AI models
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
	#firebase dashboard ID
	dashboard = "d3c4fd41-8892-453b-bc00-64d1f494284b"
	sys.exit(main(dashboard))
