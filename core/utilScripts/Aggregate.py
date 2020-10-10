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

	# setting the value of overall enforcementStatus to reflect proportion of violations
	totalEnforcementStaus = "good"
	totalVisitors = currHour["visitorCount"]
	totalViolations = currHour["violationsCount"]
	totalStatusProportion = (totalViolations*1.0)/totalVisitors
	if (totalStatusProportion > 0.7):
		totalEnforcementStaus = "critical"
	elif (totalStatusProportion > 0.3):
		totalEnforcementStaus = "medium"
	
	allStatus = currHour["enforcementStatus"]
	allStatus["status"] = totalEnforcementStaus

	# setting the value of social distancing enforcementStatus to reflect proportion of violations
	SDEnforcementStaus = "good"
	SDproportion = (currHour["undistancedCount"]*1.0) / totalVisitors
	if(SDproportion > 0.7):
		SDEnforcementStaus = "critical"
	elif(SDproportion > 0.3):
		SDEnforcementStaus = "medium"

	allStatus["socialDistancingEnforcement"] = SDEnforcementStaus

	# setting the value of face covering enforcementStatus to reflect proportion of violations
	FCEnforcementStaus = "good"
	FCproportion = (currHour["undistancedCount"]*1.0) / totalVisitors
	if(FCproportion > 0.7):
		FCEnforcementStaus = "critical"
	elif(FCproportion > 0.3):
		FCEnforcementStaus = "normal"

	allStatus["faceCoveringEnforcement"] = FCEnforcementStaus


	currHour["currTracked"] = currTracked

	# have json write this dictionary to file
	with open(filename, 'w') as f:
		json.dump(aggData, f, indent=4)

	return aggData