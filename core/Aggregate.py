import json

def genAggData(filename):
	aggData = {}
	# have json write this dictionary to file
	json.dump(aggData, filename, indent=4)