import numpy as np
import json
import math
import cv2
import pred

from torchvision import transforms, datasets

def readConfigFile(path):
	#Goal: Read contents of the config file and return the appropriate values
	#Hint: Look into json library
	with open(path,"r") as f:
		neededVars = json.load(f)

	calibration = neededVars["calibration"]
	return calibration

def runCVModel(image_path):
	#Ravit will do
	#Goal: Take an image and run inference to get depth map and bounding boxes
	#https://github.com/nianticlabs/monodepth2
	#Pytorch computer vision model
    
    """Function to predict for a single image or folder of images
    """
    depth, output = pred.predict(image_path)
    return depth, output


def getPixelDepth(pixel_coordinate_x, pixel_coordinate_y, depth_map, img, pixel_radius=10):
	#Santript, for you
	#Goal: Apply the algorithm we were discussing on finding the depth
	#	take a circle of radius pixel_radius
	#	find 50% of values of depth distribution centered at the given pixel
	#	later, we'll incorporate same solution with masks
    
    allDepth = runCVModel('test_image.jpg')
    
    #finds all the pixel coordinates of an image
    img1 = cv2.imread(img,0)
    indices = np.where(img1 != [0])
    coordinates = zip(indices[0], indices[1])
    
    #extracts all the pixels that are within a 10 pixel radius from the center pixel coordinate
    neededPixels = []
    for (pixel_x, pixel_y) in coordinates:
        if (pixel_x - pixel_coordinate_x)**2 + (pixel_y - pixel_coordinate_y)**2 <= (pixel_radius**2):
                neededPixels.append(pixel_x,pixel_y)
                
    #gets the depth of neededPixels using depth estimation
    allPixelDepth = []
    for pixels in neededPixels:
        allPixelDepth.append(allDepth[pixels])
        
    #finds the final needed depth
    length = len(allPixelDepth)
    allPixelDepth.sort()
    neededLength = int(length/2)
    neededDepth = allPixelDepth[neededLength]
        
    
    return neededDepth

def calculateCalibrationConstant(path):
	#calculating calibration information from the calibration pixel and 3D coordinates

	calibration = readConfigFile(path)

	calibPixelCoordinate = calibration["calibPixelCoordinate"]
	calib3DCoordinate = calibration["calib3DCoordinate"]

	verticalAngle = calibration["verticalAngle"]

	cameraDirection = [0, 1, -np.sin(verticalAngle)]
	cameraDirection = np.asarray(cameraDirection)

	height = calibration["cameraHeight"]
	cameraPosVector = np.asarray([0, 0, height])

	coordinate2camera  = calib3DCoordinate - cameraPosVector

	# dot product = product of magnitudes - 
	cos_angle = np.dot(cameraDirection, coordinate2camera) / (np.linalg.norm(cameraDirection) * np.linalg.norm(coordinate2camera))
	#angle = np.arccos(cos_angle)

	#Santript, for you
	#Now, all that is needed is to return calib_constant
	calib_constant = (math.sqrt(1-cos_angle*cos_angle))/cos_angle/np.linalg.norm(calibPixelCoordinate)
	#but one thing to consider... tangent(angle) = tangent(arccosine(cos_angle))
	#soooo.... it is better to rewrite np.tan(angle) as math.sqrt(1-cos_angle*cos_angle)/cos_angle

	return calib_constant

def calculate3DCoordinates(depthMap, pixelCoordinate):
	#Santript, for you
	#calculating 3D coordinates given pixel coordinate and calibration information
    
    """top_pixel_depth = getPixelDepth(topPixelCoordinate_x, topPixelCoordinate_y, "test_image.jpg", pixel_radius=10)
    bottom_pixel_depth = getPixelDepth(bottomPixelCoordinate_x, bottomPixelCoordinate_y, "test_image.jpg", pixel_radius=10)
    
    #Θ = acos(A · B) --> dot product
    vert_theta = math.acos(top_pixel_depth * bottom_pixel_depth)
    
    z_coordinate = top_pixel_depth * math.sin(vert_theta)
    
    camera_height = neededVars["calibration"]["cameraHeight"]
    bottom_hypotenuse = math.sqrt(top_pixel_depth**2 - camera_height**2)
    """
    
    #array of positions needed for pose estimation
    COCO_PERSON_KEYPOINT_NAMES = [
    'nose',
    'left_eye',
    'right_eye',
    'left_ear',
    'right_ear',
    'left_shoulder',
    'right_shoulder',
    'left_elbow',
    'right_elbow',
    'left_wrist',
    'right_wrist',
    'left_hip',
    'right_hip',
    'left_knee',
    'right_knee',
    'left_ankle',
    'right_ankle'
]
    
    with open("sample_config.json","r") as f:
    		neededVars = json.load(f)
    
    #all necessary variables from json file
    center = neededVars["calibration"]["centerpoint"]
    v = neededVars["calibration"]["verticalAngle"]
    height = neededVars["calibration"]["cameraHeight"]
    
    #finds the pixel coordinate of the nose of a person(nose just for now. It might change)
    depth,output = runCVModel("test_image.jpg")
    pixelCoordinate = depth.output["keypoints"][:][COCO_PERSON_KEYPOINT_NAMES.index("nose")]
    
    #finds the offset of object from center of image(distance)
    offset = pixelCoordinate-center
    
    #calibration constant
    k = calculateCalibrationConstant("sample_config.json")
    
    
    #needed to find the camera direction vector(how much camera has to move to have a direct view of object)
    delta_x = k * math.atan(offset[0])
    delta_y = k * math.atan(offset[1])
    
    #3D direction vector
    3DdirectionVector = [math.tan(delta_x),1,math.tan(delta_y - v)]
    
    #finds the magnitude of the 3D direction vector(needed for normalization)
    magnitude = math.sqrt(3DdirectionVector[0]**2 + 3DdirectionVector[1]**2 + 3DdirectionVector[2]**2)
    
    #uses magnitude to normalize the 3D direction vector
    normalized = 3DdirectionVector/magnitude
    
    #finds depth of pixelCoordinate using the getPixelDepth function(needed to find the actual 3D coordinates of object)
    depth = getPixelDepth(pixelCoordinate)
    
    #camera's 3D coordinates IRL
    camera_position = [0,0,height]
    
    #3D coordinates of object
    actual3DCoords = depth * normalized + camera_position
    
    
    return actual3DCoords