import numpy as np
import math
import cv2

class PixelMapper(object):
	"""
	Create an object for converting pixels to geographic coordinates,
	using four points with known locations which form a quadrilteral in both planes
	Parameters
	----------
	pixel_array : (4,2) shape numpy array
		The (x,y) pixel coordinates corresponding to the top left, top right, bottom right, bottom left
		pixels of the known region
	lonlat_array : (4,2) shape numpy array
		The (lon, lat) coordinates corresponding to the top left, top right, bottom right, bottom left
		pixels of the known region
	"""
	def __init__(self, pixel_array, lonlat_array, lonlat_origin):
		assert pixel_array.shape==(4,2), "Need (4,2) input array"
		assert lonlat_array.shape==(4,2), "Need (4,2) input array"
		self.M = cv2.getPerspectiveTransform(np.float32(pixel_array),np.float32(lonlat_array))
		self.invM = cv2.getPerspectiveTransform(np.float32(lonlat_array),np.float32(pixel_array))

		self.lonlat_origin = lonlat_origin
		self.lon_const = 40075000 * math.cos(lonlat_origin[0]*math.pi/180) / 360
		self.lat_const = 111320
        
	def pixel_to_lonlat(self, pixel):
		"""
		Convert a set of pixel coordinates to lon-lat coordinates
		Parameters
		----------
		pixel : (N,2) numpy array or (x,y) tuple
			The (x,y) pixel coordinates to be converted
		Returns
		-------
		(N,2) numpy array
			The corresponding (lon, lat) coordinates
		"""
		if type(pixel) != np.ndarray:
			pixel = np.array(pixel).reshape(1,2)
		assert pixel.shape[1]==2, "Need (N,2) input array" 
		pixel = np.concatenate([pixel, np.ones((pixel.shape[0],1))], axis=1)
		lonlat = np.dot(self.M,pixel.T)

		return (lonlat[:2,:]/lonlat[2,:]).T.tolist()
    
	def lonlat_to_pixel(self, lonlat):
		"""
		Convert a set of lon-lat coordinates to pixel coordinates
		Parameters
		----------
		lonlat : (N,2) numpy array or (x,y) tuple
			The (lon,lat) coordinates to be converted
		Returns
		-------
		(N,2) numpy array
			The corresponding (x, y) pixel coordinates
		"""
		if type(lonlat) != np.ndarray:
			lonlat = np.array(lonlat).reshape(1,2)
		assert lonlat.shape[1]==2, "Need (N,2) input array" 
		lonlat = np.concatenate([lonlat, np.ones((lonlat.shape[0],1))], axis=1)
		pixel = np.dot(self.invM,lonlat.T)

		return (pixel[:2,:]/pixel[2,:]).T.tolist()

	def lonlat_to_3D(self, lonlat):
		lon_d = lonlat[0] - self.lonlat_origin[0]
		lat_d = lonlat[1] - self.lonlat_origin[1]

		lon_m = lon_d * self.lon_const
		lat_m = lat_d * self.lat_const

		return [lat_m, lon_m, 0]
