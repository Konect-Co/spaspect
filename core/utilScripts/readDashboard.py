import os
import json

def read(dashboardID):
	dashboardInfo = {}

	top_dir = "../firebaseFiles"

	calibrationFile = os.path.join(top_dir, "calibrations", dashboardID) + ".json"
	realtimeFile = os.path.join(top_dir, "realtime", dashboardID) + ".json"
	aggregateFile = os.path.join(top_dir, "aggregate", dashboardID) + ".json"

	with open(calibrationFile, 'r') as f:
		dashboardInfo["calibration"] = json.load(f)
	with open(realtimeFile, 'r') as f:
		dashboardInfo["realtime"] = json.load(f)
	with open(aggregateFile, 'r') as f:
		dashboardInfo["aggregate"] = json.load(f)

	return dashboardInfo
