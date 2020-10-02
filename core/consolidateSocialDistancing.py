import cv2
import os
import json
import csv
import ast

locationFiles = ["Dublin", "Times Square", "Wrigley Field"]
locationIDs = ["1ff9e8ae-bfc1-11ea-b3de-0242ac130004", "0443639c-bfc1-11ea-b3de-0242ac130004", "12853b51-f36b-407f-b08d-cc53b92b0393"]

locations = []
for ID in locationIDs:
	filePath = os.path.join(os.path.dirname(os.getcwd()), "firebaseFiles", "calibrations", ID) + ".json"
	with open(filePath, 'r') as file:
		calibration = json.load(file)
		origin = calibration["lonlat_origin"]
	locations.append(origin)


with open(os.path.join(os.getcwd(), "csvFiles", "CrossLocationData") + ".csv", 'w', newline="") as wf:
	outCSV = csv.writer(wf)

	outCSV.writerow(["name", "avgDist", "lat", "lon"])
	for i in range(len(locationFiles)):
		
		locationFile = locationFiles[i]
		location = locations[i]

		filePath = os.path.join(os.getcwd(), "csvFiles", locationFile) + ".csv"
		
		countSum = 0
		distancesSum = 0

		with open(filePath, 'r') as rf:
			rf.__next__()
			inCSV = csv.reader(rf)
			for row in inCSV:
				distances = ast.literal_eval(row[2])
				if (len(distances) == 0):
					continue

				distanceAvg = sum(distances)/len(distances)

				countSum += 1
				distancesSum += distanceAvg

		if (countSum != 0):
			distanceVal = distancesSum/countSum
			outCSV.writerow([locationFile, distanceVal, location[0], location[1]])