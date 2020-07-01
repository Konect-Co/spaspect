import json
import streamlink
import time
import math
import sys
import utils
import numpy as np
import cv2
import matplotlib.pyplot as plt

import PixelMapper
import TrackedObject
from cv_model import pred

def main(config_info):
	imagePath = config_info["imagePath"]
	outputPath = config_info["outputPath"]
	streamLink = config_info["streamLink"]
	configPath = config_info["configPath"]
	video = config_info["isVideo"]

	cap = cv2.VideoCapture()
	cap.open(streamLink)

	pm = PixelMapper.PixelMapper.fromfile(configPath)

	video = True
	frame_rate = cv2.CAP_PROP_FPS

	for _ in range(100):
		cap.read()

	while True:
		print("FRAME")
		read, image = cap.read()
		if (not read):
			print("END")
			break

		cv2.imwrite(imagePath, image)
		output = pred.predict(imagePath)
		TrackedObject.TrackedObject.track(output["boxes"])
		print(TrackedObject.TrackedObject.objects)

		predOutput = utils.makeVisualizationOutput(pm, output)
		with open(outputPath, 'w') as file:
			file.write(json.dumps(predOutput))

		startTime = time.time()
		interval = int(time.time()-startTime)
		if (interval<5):
			time.sleep(5-interval)
			interval = 5
		if (video):
			for _ in range(interval*frame_rate):
				cap.read()

	return 0

if __name__ == "__main__":
	args = {
		"imagePath":"/home/ravit/Pictures/Frame.jpg",
		"outputPath":"/home/ravit/Konect-Code/spaspect-project/spaspect/visualization/browser-demo/output.json",
		"configPath":"/home/ravit/Konect-Code/spaspect-project/spaspect/visualization/browser-demo/config.json",
		"streamLink":"/home/ravit/Videos/TimesSquare2.mp4",
		"isVideo":True
	}
	sys.exit(main(args))
