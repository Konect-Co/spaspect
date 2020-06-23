import cv2
import numpy as np
import math

def add(a, b):
    return a+b

def _readImage(imagePath):
    image = cv2.imread(imagePath)
    return image

def _calculateCalibrationConstant(verticalAngle, height, calibPixelCoordinate, calib3DCoordinate):
    cameraDirection = np.asarray([0, 1, -np.sin(verticalAngle)])
    cameraPosVector = np.asarray([0, 0, height])
    coordinate2camera  = calib3DCoordinate - cameraPosVector

    cosAngle = np.dot(cameraDirection, coordinate2camera) / (np.linalg.norm(cameraDirection) * np.linalg.norm(coordinate2camera))

    calibConstant = (math.sqrt(1-cosAngle*cosAngle)/cosAngle)/np.linalg.norm(calibPixelCoordinate)

    return calibConstant

def _getPixelDepth(pixelCoordinate, depthMap, pixelRadius=10):
    pixelCoordinateX = pixelCoordinate[0]
    pixelCoordinateY = pixelCoordinate[1]
    
    #extracts all the pixels that are within a 10 pixel radius from the center pixel coordinate
    neededPixels = np.asarray([])
    for pixelX in range(pixelCoordinateX-pixelRadius, pixelCoordinateX+pixelRadius):
        for pixelY in range(pixelCoordinateY-pixelRadius, pixelCoordinateY+pixelRadius):
            if (pixelX - pixelCoordinateX)**2 + (pixelY - pixelCoordinateY)**2 <= (pixelRadius**2):
                    neededPixels.append(pixelX,pixelY)
                
    #gets the depth of neededPixels using depth estimation
    pixelDepths = []
    for pixels in neededPixels:
        pixelDepths.append(depthMap[pixels])
    
    #finds the final needed depth
    length = len(pixelDepths)
    pixelDepths.sort()
    neededLength = int(length/2)
    neededDepth = pixelDepths[neededLength]

    return neededDepth

def _calculateSpatialCoordinate(pixelCoordinate, center, verticalAngle, k, height, depthMap, pixelRadius):
    #finds the offset of object from center of image(distance)
    offset = pixelCoordinate-center

    #needed to find the camera direction vector(how much camera has to move to have a direct view of object)
    delta_x = k * math.atan(offset[0])
    delta_y = k * math.atan(offset[1])

    #3D direction vector
    directionVector = [math.tan(delta_x), 1, math.tan(delta_y - verticalAngle)]

    #finds the magnitude of the 3D direction vector(needed for normalization)
    magnitude = math.sqrt(directionVector[0]**2 + directionVector[1]**2 + directionVector[2]**2)

    #uses magnitude to normalize the 3D direction vector
    normalized = directionVector/magnitude

    #finds depth of pixelCoordinate using the getPixelDepth function(needed to find the actual 3D coordinates of object)
    depth = _getPixelDepth(pixelCoordinate, depthMap, pixelRadius=pixelRadius)

    #camera's 3D coordinates IRL
    camera_position = [0,0,height]

    #3D coordinates of object
    actual3DCoord = depth * normalized + camera_position

    return actual3DCoord