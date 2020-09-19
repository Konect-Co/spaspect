import json


"""
Generates the aggregate data displayed on SpaSpect dashboard

@params CVOutput, filename
@return aggregate data
"""
def genAggData(CVOutput, filename):
	#TODO: Add a new field every hour
	# loading aggregate data from file
	with open(filename, 'r') as f:
		aggData = json.load(f)

	hoursList = list(aggData.keys())
	hoursList.sort(reverse=True)
	currHour = aggData[hoursList[0]]

	currTracked = currHour["currTracked"]
	tracked = CVOutput["tracked"]

	# looping through the tracked objects
	for trackedObj in CVOutput["tracked"].values():
		name = trackedObj["name"]
		#TODO: Aggregate should perhaps be calculated at the end of each hour
		if (name not in currTracked):
			currTracked.append(name)
			currHour["visitorCount"] += 1

			unmasked = True if trackedObj["masked"] == 2 else False
			undistanced = True if trackedObj["distanced"] == 0 else False
			violation = unmasked or undistanced

			if (unmasked):
				currHour["unmaskedCount"] += 1
			if (undistanced):
				currHour["undistancedCount"] += 1
			if (violation):
				currHour["violationsCount"] += 1

			#TODO: Handle currHour["averageDistance"]

	currHour["currTracked"] = currTracked

	# have json write this dictionary to file
	with open(filename, 'w') as f:
		json.dump(aggData, f, indent=4)

	return aggData