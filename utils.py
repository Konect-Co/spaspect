#finds the dot product between two vectors
def dotProduct(vector1, vector2):
	assert len(vector1) == len(vector2)
	
	dotProd = 0
	for i in len(vector1):
		dotProd += vector1[i]*vector2[i]
	
	return dotProd

#finds the tip-tail sum of the two vectors
def add(vector1, vector2):
	addedVector = []

	assert len(vector1) == len(vector2)

	for i in len(vector1):
		addedVector += [vector1[i] + vector2[i]]
	
	return addedVector

#scales the vector by a particular factor
def scale(vector, factor):
	for i in len(vector):
		vector[i] = vector[i]*factor
	
	return vector

#gets the length of a vector
def length(vector):
	length = 0
	for i in len(vector):
		length += vector[i]**2
	length = math.sqrt(length)

	return length

#normalizes the vector
def normalize(vector):
	vector = scale(vector, 1/length(vector))
	return vector

#finds the angle between two vectors
def findAngle(vector1, vector2):
	cosVal = dotProd(vector1, vector2)/(length(vector1)*length(vector2))
	angle = math.acos(cosVal)
	return cosVal

#finds the intersection between a line and plane
def findIntersection(height, LineDirection):
	#Assume LinePoint is [0,0,height] as it is the location of the camera
	LinePoint = [0, 0, height]
	
	#Assume PlanePoint is [0,0,0] and PlaneDirection is [0, 0, 1]
	#PlaneDirection means the vector normal to the plane
	PlanePoint = [0, 0, 0]
	PlaneDirection = [0, 0, 1]

	assert dotProduct(planeDirection, normalize(LineDirection)) != 0

	#Source: https://stackoverflow.com/questions/5666222/3d-line-plane-intersection
	t = (dotProd(PlaneDirection, PlanePoint) - dotProd(PlaneDirection, LinePoint)) / dotProduct(PlaneDirection, normalize(LineDirection))
	intersection = add(LinePoint, scale(normalize(LineDirection), t))

	return intersection
