#pragma once

#include <map>
#include <iostream>
#include <string>
#include <opencv2/opencv.hpp>
#include "TrackedObject.h"

using namespace std;

//Data structure that stores information about the object
class locationInfo {
public:
	float coordinate[3];
	float boundingbox[4];
	float latlon[2];
	bool distanced;
	bool masked;
}

//Data structure that represents the dashboard
class dashboard {
private:
	class TrackedEntity {
	public:
		float lastUpdate;
		std::map<int, locationInfo> history;
	};
public:
	string streamlink;
	string name;
	class {
	public:
		float lat_vals[4];
		float lon_vals[4];
		float lonlat_origin[2];
		int pixelX_vals[4];
		int pixelY_vals[4];
	} calibration;

	class {
	public:
		int coordinates[][3];
		int distanced[];
		int latlonvals[][2];
		int masked[];
	} output;

	std::vector<TrackedEntity> objects;
}