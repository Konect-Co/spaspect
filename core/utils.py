import cv2
import numpy as np
import math

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
    #neededPixels = np.asarray([])
    neededPixels = []
    for pixelX in range(int(pixelCoordinateX-pixelRadius), int(pixelCoordinateX+pixelRadius)):
        for pixelY in range(int(pixelCoordinateY-pixelRadius), int(pixelCoordinateY+pixelRadius)):
            if (pixelX - pixelCoordinateX)**2 + (pixelY - pixelCoordinateY)**2 <= (pixelRadius**2):
                    #np.append(neededPixels,(pixelX,pixelY))
                    neededPixel = [pixelX,pixelY]
                    neededPixels.append(neededPixel)
                
    #gets the depth of neededPixels using depth estimation
    pixelDepths = []
    neededPixelsLength = len(neededPixels)
    for i in range(neededPixelsLength):
        neededPixelX = neededPixels[i][0]
        neededPixelY = neededPixels[i][1]
        pixelDepths.append(depthMap[neededPixelX][neededPixelY])
    
    #finds the final needed depth
    #print("neededPixels: ",neededPixels)
    #print("Depth map: ",depthMap)
    #print("Pixel depths: ",pixelDepths)
    length = len(pixelDepths)
    #print("length of pixelDepths: ",length)
    pixelDepths.sort()
    #print("PixelDepths after sorting: ",pixelDepths)
    neededLength = int(length/2)
    #print("Needed length: ",neededLength)
    neededDepth = pixelDepths[neededLength]

    return neededDepth

def _calculateSpatialCoordinate(pixelCoordinate, center, verticalAngle, k, height, depthMap, pixelRadius):
    #finds the offset of object from center of image(distance)
    pkShape = pixelCoordinate.shape
    offset = pixelCoordinate-center#.reshape(pkShape)

    #needed to find the camera direction vector(how much camera has to move to have a direct view of object)
    delta_x = k * math.atan(offset[0])
    delta_y = k * math.atan(offset[1])

    #3D direction vector
    directionVector = np.array([math.tan(delta_x), 1, math.tan(delta_y - verticalAngle)])

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