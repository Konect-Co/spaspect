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

	for _ in range(100):
		cap.read()

	while True:
		print("FRAME", frame_index, "##############")
		#pixels = pm.getPixels()
		#print('Pixel array:', end="")
		#for pixel in pixels:
		#	print(pixel, end=" ")
		#print('')
		
		read, image = cap.read()
		if (not read):
			print("END")
			break
		framePath = os.path.join(imagePath,"Frame_" + str(frame_index) + ".jpg")
		cv2.imwrite(framePath, image)
		output = pred.predict(framePath)
		TrackedObject.TrackedObject.track(output["boxes"])

		predOutput = utils.makeVisualizationOutput(pm, output)

		maskList = predOutput["wearingMasks"]
		latlongList = predOutput["lat-long"]
		#coordList = predOutput["3DCoordinates"]
		print("Masks (0=uncertain, 1=masked, 2=unmasked) and Coordinates: ")
		for i in range(0,len(maskList)):
			print(maskList[i], "at:\t", latlongList[0][i], latlongList[1][i])
		print('')
		
		frameImage = cv2.imread(framePath)
		boxes = predOutput["Boxes"]
		faceBoxes = predOutput["Faces"]
		for boxList in boxes:
			for box in boxList:
				cv2.rectangle(frameImage, (int(box[0]+0.5), int(box[1]+0.5)), (int(box[2]+0.5), int(box[3]+0.5)), (0,0,255), 2)
		for boxList in faceBoxes:
			for box in boxList:
				cv2.rectangle(frameImage, (int(box[0]+0.5), int(box[1]+0.5)), (int(box[2]+0.5), int(box[3]+0.5)), (255,0,0), 2)
		cv2.imwrite(framePath, frameImage)
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

if __name__ == "__main__":
	args = {
		"imagePath":"/mnt/d/Konect/spaspect/Frames", #changed this to save all the frames in one folder
		"outputPath":"/mnt/d/Konect/spaspect/visualization/browser-demo/output.json",
		"configPath":"/mnt/d/Konect/spaspect/visualization/browser-demo/config.json",
		"streamLink":"/mnt/d/Konect/spaspect/core/TEMPDATA_Testing-Track-Function/TimesSquare2.mp4",
		"isVideo":True
	}
	sys.exit(main(args))
