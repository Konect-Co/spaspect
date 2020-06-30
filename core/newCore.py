import newUtils
import numpy as np
import cv2
import matplotlib.pyplot as plt
from cv_model import pred
import json
import streamlink
import time
import math

quad_coords = {
    "lonlat": np.array([
        [40.759271, -73.984976], # left side of tkts
        [40.759316, -73.985132], # left back bottom corner of bench
        [40.759196, -73.985201], # right front bottom corner of bench
        [40.759104, -73.985035] # right side of tkts
    ]),
    "pixel": np.array([
        [330, 250], # left side of tkts
        [50, 370], # left back bottom corner of bench
        [945,395], # right front bottom corner of bench
        [815,245] # right side of tkts
    ]),
	"lonlat_origin": [40.759260, -73.985235]
}

pm = newUtils.PixelMapper(quad_coords["pixel"], quad_coords["lonlat"], quad_coords["lonlat_origin"])

imagePath = "/home/ravit/Pictures/Frame.jpg"
jsonPath = "/home/ravit/Konect-Code/spaspect-project/spaspect/visualization/browser-demo/test.json"
score_threshold = 0.80

"""streamLink = streamlink.streams("https://www.earthcam.com/usa/newyork/timessquare/?cam=tsstreet")
streamLink = streamLink[list(streamLink.keys())[0]].url"""

streamLink = "/home/ravit/Videos/TimesSquare2.mp4"
cap = cv2.VideoCapture()
cap.open(streamLink)

video = True
frame_rate = cv2.CAP_PROP_FPS

for _ in range(100):
	cap.read()

while True:
	read, image = cap.read()
	if (not read):
		print("END")
		break

	startTime = time.time()

	cv2.imwrite(imagePath, image) 
	#image = cv2.imread(imagePath)
	output = pred.predict(imagePath)

	coords3D = []
	long_lats = []
	for i in range(len(output["boxes"])):
		if (output["scores"][i] < score_threshold):
			break
		box = output["boxes"][i]
		
		midpoint = [int((box[0]+box[2])/2), box[3]]

		long_lat = pm.pixel_to_lonlat(midpoint)[0]
		coord3D = pm.lonlat_to_3D(long_lat)

		long_lats.append(long_lat)
		coords3D.append(coord3D)

		#image = cv2.rectangle(image, (box[0], box[1]), (box[2], box[3]), (255,0,0), 2)
		#image = cv2.circle(image, midpoint, 1, (255,0,0))

	if (coords3D != []):
		long_lats = np.swapaxes(np.asarray(long_lats), 0, 1).tolist()
		coords3D = np.asarray(coords3D).tolist()

	safe = [1] * len(coords3D)
	threshold = 2	
	for i in range(len(coords3D)):
		for j in range(i+1, len(coords3D)):
			if (safe[i] == 0 and safe[j] == 0):
				continue
			assert len(coords3D[i]) == len(coords3D[j])
			distance = math.sqrt(sum(e**2 for e in [coords3D[i][k]-coords3D[j][k] for k in range(2)]))
			if (distance < threshold):
				safe[i] = 0
				safe[j] = 0

	predOutput = {"3DCoordinates":coords3D, "lat-long":long_lats, "safe":safe}
	with open(jsonPath, 'w') as file:
		file.write(json.dumps(predOutput))
	break
	interval = int(time.time()-startTime)
	if (interval<5):
		time.sleep(5-interval)
		interval = 5
	if (video):
		for _ in range(interval*frame_rate):
			cap.read()

"""image_bgr = image[:,:,[2,1,0]]
plt.imshow(image_bgr)
plt.show()"""
