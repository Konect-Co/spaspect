import os
import sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

from core import PixelMapper
from core.cv_model import utils

def testcases_PixelMapper():
	pixel_coords = [[330,250],[50,370],[945,395],[815,245]]
	lonlat_coords = [[-73.984976, 40.759271],[-73.985132, 40.759316], [-73.985201, 40.759196],[-73.985035,40.759104]]

	pm = PixelMapper.PixelMapper(pixel_coords, lonlat_coords, lonlat_coords[0])

	lonlat = pm.pixel_to_lonlat([100,200])
	pixel = pm.lonlat_to_pixel([-73.985, 40.7592])
	_3D = pm.lonlat_to_3D([-73.985, 40.7592])
	lonlat2 = pm._3D_to_lonlat([10,10,0])

def testcases_CVUtils():
	boxA = [50,50,100,100]
	boxB = [100,100,100,100]

	areaA = utils.computeArea(boxA)
	areaB = utils.computeArea(boxB)
	intersection = utils.computeIntersection(boxA, boxB)
	IoU = utils.computeIOU(boxA, boxB)
	IoA = utils.computeIOA(boxA, boxB)

	print(areaA, areaB, intersection, IoU, IoA)