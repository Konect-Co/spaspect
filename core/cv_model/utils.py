#box format: [x, y, height, width] where (x,y) is the top left corner

#this function computes the area of a box
def computeArea(box):
	box_reformed = [box[0], box[1], box[0]+box[2], box[1]+box[3]]
	return (box_reformed[2]-box_reformed[0])*(box_reformed[3]-box_reformed[1])

#this function computes the intersection between two boxes
def computeIntersection(boxA, boxB):
	boxA_reformed = [boxA[0], boxA[1], boxA[0]+boxA[2], boxA[1]+boxA[3]]
	boxB_reformed = [boxB[0], boxB[1], boxB[0]+boxB[2], boxB[1]+boxB[3]]

	#cases to return 0
	if (boxB_reformed[0]>boxA_reformed[2] or boxA_reformed[0]>boxB_reformed[2] or boxB_reformed[1]>boxA_reformed[3] or boxA_reformed[1]>boxB_reformed[3]):
		return 0

	#determining the X and Y values
	xVals = [boxA_reformed[0], boxA_reformed[2], boxB_reformed[0], boxB_reformed[2]]
	yVals = [boxA_reformed[1], boxA_reformed[3], boxB_reformed[1], boxB_reformed[3]]
	#arranging from least to greatest
	xVals.sort()
	yVals.sort()
	
	#returning intersection
	intersection = (xVals[2]-xVals[1])*(yVals[2]-yVals[1])
	return intersection

#this function computes the IoU between two boxes
def computeIOU (boxA, boxB):

	#computing intersection from above method
	intersection = computeIntersection(boxA, boxB)
	#computing area from above method
	union = computeArea(boxA) + computeArea(boxB) - intersection
	iou = intersection/union

	#returning IOU
	return iou

#this function computes Intersection over Area of A
def computeIOA (boxA, boxB):
	intersection = computeIntersection(boxA, boxB)
	aArea = computeArea(boxA)
	iou = intersection/aArea

	#returning IOA
	return iou
