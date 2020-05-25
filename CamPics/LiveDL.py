import streamlink
import cv2
import time

camLinks = {
	"Location1":"https://www.earthcam.com/usa/newyork/timessquare/?cam=tsstreet",
	"Location2":"https://www.earthcam.com/usa/newyork/timessquare/?cam=tsrobo3"
}

streamLinks = {}
for location in camLinks.keys():
	streamLinks[location] = streamlink.streams(camLinks[location])['720p'].url #assuming there is a 720p option

#streams = streamlink.streams("https://www.earthcam.com/usa/newyork/timessquare/?cam=tsstreet")

cap = cv2.VideoCapture()

while True:
	start_time = time.time()

	for location in streamLinks.keys():
		streamLink = streamLinks[location]
		cap.open(streamLink)
		_, frame = cap.read()
		cv2.imwrite(location + ".jpg", frame)
	
	#sleep until 3 seconds are complete from the starting of the capture
	duration = 3-(time.time()-start_time)
	if (duration>0):	
		time.sleep(duration)
