import json


"""
Generates the aggregate data displayed on SpaSpect dashboard

@params CVOutput, filename
@return aggregate data
"""
def genAggData(CVOutput, filename):
	with open(filename, 'r') as f:
		aggData = json.load(f)

	hoursList = list(aggData.keys())
	hoursList.sort(reverse=True)
	currHour = aggData[hoursList[0]]

	tracked = CVOutput["tracked"]

	#TODO: This should be looking at tracked individuals not raw boxes
	currHour["visitorCount"] += len(CVOutput["distanced"])
	currHour["undistancedCount"] += 2
	currHour["unmaskedCount"] += 2
	currHour["violationsCount"] += 2
	currHour["averageDistance"] += 0.1
	currHour["currTracked"] = tracked

	# have json write this dictionary to file
	with open(filename, 'w') as f:
		json.dump(aggData, f, indent=4)
	return aggData