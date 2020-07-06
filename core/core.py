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

root_dir = "/home/ravit/Konect-Code/spaspect-project/spaspect/visualization"

def main(config_info):
	imagePath = config_info["imagePath"]
	configPath = config_info["configPath"]
	video = config_info["isVideo"]

	with open(configPath, 'r') as f:
		config = json.loads(f.read())
		streamLink = os.path.join(root_dir, config["video-source"])
		outputPath = os.path.join(root_dir, config["output-file"])

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
		
		#TODO: This should not override the config file but add to it
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
		"configPath":"/home/ravit/Konect-Code/spaspect-project/spaspect/visualization/config/TimesSquare.json",
		"isVideo":True
	}
	sys.exit(main(args))