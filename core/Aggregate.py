import json


"""
Generates the aggregate data displayed on SpaSpect dashboard

@params filename
@return aggregate data
"""
def genAggData(filename):
	aggData = {}
	# have json write this dictionary to file
	json.dump(aggData, filename, indent=4)