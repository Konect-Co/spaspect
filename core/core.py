import json
import streamlink
import time
import math
import sys
import utils
import numpy as np
import cv2
import os
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
	frame_index = 0

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


root_path = "/home/ravit/Konect-Code/spaspect-project/spaspect"
if __name__ == "__main__":
	args = {
		"imagePath":"/home/ravit/Pictures/Frame.jpg",
		"outputPath":os.path.join(root_path, "visualization", "browser-demo", "output.json"),
		"configPath":os.path.join(root_path, "visualization", "browser-demo", "config.json"),
		"streamLink":"/home/ravit/Videos/TimesSquare2.mp4",
		"isVideo":True
	}
	sys.exit(main(args))