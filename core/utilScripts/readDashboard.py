import os
import json

def read(dashboardID):
	dashboardInfo = {}

	top_dir = "../../firebaseFiles"

	dashboardInfo["calibration"] = json.load(os.path.join(top_dir, "calibration", dashboardID) + ".json") 
	dashboardInfo["realtime"] = json.load(os.path.join(top_dir, "realtime", dashboardID) + ".json")
	dashboardInfo["aggregate"] = json.load(os.path.join(top_dir, "aggregate", dashboardID) + ".json")

	return dashboardInfo
