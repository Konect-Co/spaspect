#box format: [x, y, height, width] where (x,y) is the top left corner

#this function computes the area of a box
def computeArea(box):
	box_reformed = [box[0], box[1], box[0]+box[2], box[1]+box[3]]
	return (box_reformed[2]-box_reformed[0])*(box_reformed[3]-box_reformed[1])

#this function computes the intersection between two boxes
def computeIntersection(boxA, boxB):
	boxA_reformed = [boxA[0], boxA[1], boxA[0]+boxA[2], boxA[1]+boxA[3]]
	boxB_reformed = [boxB[0], boxB[1], boxB[0]+boxB[2], boxB[1]+boxB[3]]

	if (boxB_reformed[0]>boxA_reformed[2] or boxA_reformed[0]>boxB_reformed[2] or boxB_reformed[1]>boxA_reformed[3] or boxA_reformed[1]>boxB_reformed[3]):
		return 0

	xVals = [boxA_reformed[0], boxA_reformed[2], boxB_reformed[0], boxB_reformed[2]]
	#print("xVals: ",xVals)
	yVals = [boxA_reformed[1], boxA_reformed[3], boxB_reformed[1], boxB_reformed[3]]
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
