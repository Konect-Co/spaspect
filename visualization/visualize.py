from mpl_toolkits.mplot3d import Axes3D
import json

import os
import sys

import matplotlib.pyplot as plt
import numpy as np

fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')

'''ax.set_xlabel('X Label')
ax.set_ylabel('Y Label')
ax.set_zlabel('Z Label')'''

fig_overhead = plt.figure()

if __name__ == "__main__":
	try:
		path = str(sys.argv[1])
	except:
		print("Usage: python " + sys.argv[0] + " coordinates_path")
		sys.exit(1)

	print(path)
	
	if (not os.path.exists(path)):
		raise Exception("Specified file does not exist.")

	try:
		with open(path) as f:
			coordinates = json.loads(f.read())
		person_coordinates = coordinates["person_coordinates"]
		car_coordinates = coordinates["car_coordinates"]

		for coordinate in person_coordinates:
			ax.scatter(coordinate[0], coordinate[1], coordinate[2], marker='o')
		for coordinate in car_coordinates:
			ax.scatter(coordinate[0], coordinate[1], coordinate[2], marker='^')
		
		plt.show()
	except:
		raise Exception("Error in parsing file. Please check file and try again.")
