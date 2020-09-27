import numpy as np
import cv2
import json
import math

"""
Create an object for converting pixels to geographic coordinates,
using four points with known locations which form a quadrilteral in both planes
"""
class PixelMapper(object):
	def __init__(self, pixel_array, lonlat_array, lonlat_origin):
		#converting pixel and lonlat array to numpy array
		pixel_array = np.array(pixel_array)
		lonlat_array = np.array(lonlat_array)

		#identifying shape of arrays
		assert pixel_array.shape==(4,2), "Need (4,2) input array"
		assert lonlat_array.shape==(4,2), "Need (4,2) input array"

		#Calculates a perspective transform from four pairs of the corresponding points
		self.M = cv2.getPerspectiveTransform(np.float32(pixel_array),np.float32(lonlat_array))
		self.invM = cv2.getPerspectiveTransform(np.float32(lonlat_array),np.float32(pixel_array))
		
		#defining a few variables needed for conversions
		self.lonlat_origin = lonlat_origin
		self.lon_const = 40075000 * math.cos(lonlat_origin[0]*math.pi/180) / 360
		self.lat_const = 111320
        
	def pixel_to_lonlat(self, pixel):
		"""
		Convert a set of pixel coordinates to lon-lat coordinates
		"""
		#checking if pixel is of type np.ndarray and alters shape if not
		if type(pixel) != np.ndarray:
			pixel = np.array(pixel).reshape(1,2)
		assert pixel.shape[1]==2, "Need (N,2) input array" 
		#Joining the sequence of arrays along an existing axis
		pixel = np.concatenate([pixel, np.ones((pixel.shape[0],1))], axis=1)
		#calculating dot product of M and pixel.T, which is the lonlat coordinates
		lonlat = np.dot(self.M,pixel.T)

		#returning lonlat coordinates
		return (lonlat[:2,:]/lonlat[2,:]).T.tolist()
    
	def lonlat_to_pixel(self, lonlat):
		"""
		Convert a set of lon-lat coordinates to pixel coordinates
		"""
		#checking if lonlat is of type np.ndarray and alters shape if not
		if type(lonlat) != np.ndarray:
			lonlat = np.array(lonlat).reshape(1,2)
		assert lonlat.shape[1]==2, "Need (N,2) input array" 
		#Joining the sequence of arrays along an existing axis
		lonlat = np.concatenate([lonlat, np.ones((lonlat.shape[0],1))], axis=1)
		#calculating dot product of invM and lonlat.T, which are the pixel coordinates
		pixel = np.dot(self.invM,lonlat.T)

		#returning pixel coordinates
		return (pixel[:2,:]/pixel[2,:]).T.tolist()

	def lonlat_to_3D(self, lonlat):
		"""
		Convert a set of lon-lat coordinates to 3D coordinates
		"""
		lon_d = lonlat[0] - self.lonlat_origin[0]
		lat_d = lonlat[1] - self.lonlat_origin[1]

		lon_m = lon_d * self.lon_const
		lat_m = lat_d * self.lat_const

		#returning 3D coordinates
		return [lat_m, lon_m, 0]

	def _3D_to_lonlat(self, _coords3D):
		"""
		Convert a set of 3D coordinates to lon-lat coordinates
		"""
		lon_m = _coords3D[1]
		lat_m = _coords3D[0]
		
		lon_d = lon_m / self.lon_const
		lat_d = lat_m / self.lat_const
		
		lon_coord = lon_d + self.lonlat_origin[0]
		lat_coord = lat_d + self.lonlat_origin[1]
		
		#returning lon and lat coordinates
		return [lon_coord, lat_coord]
