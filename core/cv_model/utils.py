#this function computes the area of a box
def computeArea(box):
	return (box[2]-box[0])*(box[3]-box[1])

#this function computes the intersection between two boxes
def computeIntersection(boxA, boxB):
	if (not ((boxB[2]>boxA[0] and boxA[2]>boxB[0]) or (boxA[2]>boxB[0] and boxB[2]>boxA[0])) and
		((boxB[3]>boxA[1] and boxA[3]>boxB[1]) or (boxA[3]>boxB[1] and boxB[3]>boxA[1]))):
		return 0

	xVals = [boxA[0], boxA[2], boxB[0], boxB[2]]
	#print("xVals: ",xVals)
	yVals = [boxA[1], boxA[3], boxB[1], boxB[3]]
	#print("yVals: ",yVals)
	xVals.sort()
	yVals.sort()
	
	#print("New xVals: ",xVals)
	#print("New yVals: ",yVals)
	intersection = (xVals[2]-xVals[1])*(yVals[2]-yVals[1])
	return intersection

#this function computes the IoU between two boxes
def computeIOU (boxA, boxB):
	intersection = computeIntersection(boxA, boxB)

	union = computeArea(boxA) + computeArea(boxB) - intersection

	iou = intersection/union

	return iou

#this function computes Intersection over Area of A
def computeIOA (boxA, boxB):
	intersection = computeIntersection(boxA, boxB)
	#print("Intersection: ",intersection)

	aArea = computeArea(boxA)
	#print("area of boxA: ",aArea)
	iou = intersection/aArea

	return iou
