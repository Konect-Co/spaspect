# Spaspect Modularity

## core technology overview
- configuration organization
	- config file
		- metadata information (location, which cam, earthcam link, image resolution)
			- calibration information
		- 3D map
			- timestamp
			- for each object
				category
				3D coordinate
- processing image data
	- reading calibration data from config file
	- making depth map
	- making 3D coordinates
		- inputs: bounding box output, calibration info, depth map (, past 3D coordinates info)

## vizualization/GUI overview
- enable constructing new configuration settings
	- GUI enabling one to build a new config file by specifying required information
- 3D map: live vizualization of the outputs
	- visualizing the 3D map of people and objects
	- visualizing the 2D overhead map
	- integrating with GIS data
		- Overlaying predictions with Google Maps data
