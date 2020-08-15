// Copyright 2020 The Konect SpaSpect Authors. All Rights Reserved.
// This file is part of Konect SpaSpect technology.
//  ___            ___              _   
// / __|_ __  __ _/ __|_ __  ___ __| |_ 
// \__ \ '_ \/ _` \__ \ '_ \/ -_) _|  _|
// |___/ .__/\__,_|___/ .__/\___\__|\__|
//     |_|            |_|               
#pragma once

#include <map>
#include <iostream>
#include <string>
#include <cmath>
#include <opencv2/opencv.hpp>
//#include "tensorflow/tensorflow/cc/saved_model/loader.h"
#include <cassert>
#include <array>
#include <algorithm>
//#include <cv.h>
#include <vector>
#include "NumCpp.hpp"
#include <opencv2/core/types.hpp>

using namespace std;
using namespace cv;

/*
namespace Track {
	struct locationInfo {
		int boundingBox[4];
		int _3DCoordinate[3];
		int lonlatCoordinate[2];
	}
	class TrackedEntity {
	public:
		static unsigned float currTime = 0;

		unsigned float lastUpdate;
		float velocity[2];
		map<int, locationInfo> history;

		TrackedEntity():lastUpdate(currTime), velocity({0, 0}, history(std::map<int, locationInfo>())) {}
		void addNext(float time, locationInfo &newLocationInfo) {
			history[time] = newLocationInfo;

			//update velocity
			int newBoxCenter[2] = {static_cast<int>(newLocationInfo.boundingBox[0] + newLocationInfo.boundingBox[2]/2.), 
				static_cast<int>(newLocationInfo.boundingBox[1] + newLocationInfo.boundingBox[3]/2.)};
			int currBoxCenter[2] = {static_cast<int>(boundingBox[0] + boundingBox[2]/2.), 
				static_cast<int>(boundingBox[1] + boundingBox[3]/2.)};
			velocity = {static_cast<int>((newBoxCenter[0]-currBoxCenter[0]*1.) / (currTime-lastUpdate)), 
				static_cast<int>((newBoxCenter[1]-currBoxCenter[1]*1.) / (currTime-lastUpdate))};
		}
		//Computes the prediction of the next bounding box using velocity and current position

		int[4] estimateBB() {
			float timeDiff = currTime - lastUpdate;
			float deltaX = velocity[0]*timeDiff;
			float deltaY = velocity[1]*timeDiff;

			int currBB[4] = history[history.end()-1].boundingBox;
			int newBB[4] = {currBB[0]+deltaX, currBB[1]+deltaY, currBB[2]+deltaX, currBB[3]+deltaY};
			return newBB;
		}
		static void updateTime() {
			currTime = std::time(0);
		}
		static void track(dashboard &dash, std::vector<DashboardInfo::locationInfo*>) {
			//TODO
		}

		static void prune(dashboard &dash) {
			//TODO
		}
	};
} //namespace Track

namespace DashboardInfo {
	//Data structure that stores information about the object
	class locationInfo {
	public:
		float coordinate[3];
		float boundingbox[4];
		float latlon[2];
		bool distanced;
		bool masked;
	};

	//Data structure that represents the dashboard
	class dashboard {
	public:
		string streamlink;
		string name;
		vector<Track::TrackedEntity*> objects;

		class {
		public:
			float lon_vals[4];
			float lat_vals[4];			
			float lonlat_origin[2];
			int pixelX_vals[4];
			int pixelY_vals[4];
		} calibration;

		bool addTrackedObject(Track::TrackedEntity* object) {
			//TODO: Add checks
			objects.push_back(object);
			return true;
		}

		bool removeTrackedObject(Track::TrackedEntity* object) {
			int obj_pos = find(begin(objects), end(objects), object) - begin(objects);
			//cout<<obj_pos<<endl;
			if (obj_pos != end(objects)) {
				objects.erase(obj_pos);
				return true;
			}
			return false;
		}
	};

} //namespace DashboardInfo
*/
namespace PixelMapper {
	class PixelMapperConfig {
	public:
	  Point2f pixel_array[4];
	  Point2f lonlat_array[4];

	  Point2f* lonlat_origin;

	  float lat_const;
	  float lon_const;

	  Mat M;
	  Mat invM;
	  
	  PixelMapperConfig(Point2f (&pixel_array)[4], Point2f (&lonlat_array)[4], Point2f* (&lonlat_origin))
	  : lonlat_origin(lonlat_origin) {
	  	this->lat_const = 111320.;
	    this->lon_const = 40075000 * cos(lonlat_origin->x * M_PI / 180) / 360;

	    this->pixel_array[0] = pixel_array[0];
	    this->pixel_array[1] = pixel_array[1];
	    this->pixel_array[2] = pixel_array[2];
	    this->pixel_array[3] = pixel_array[3];

	    this->lonlat_array[0] = lonlat_array[0];
	    this->lonlat_array[1] = lonlat_array[1];
	    this->lonlat_array[2] = lonlat_array[2];
	    this->lonlat_array[3] = lonlat_array[3];

		this->M = getPerspectiveTransform(pixel_array, lonlat_array);
		this->invM = getPerspectiveTransform(lonlat_array, pixel_array);
	  }
	};

	// Convert a set of pixel coordinates to lon-lat coordinates
	std::vector<Point2f*>* pixel_to_lonlat(PixelMapperConfig &config, std::vector<Point2f*>& pixel_coordinates) {
		int N = pixel_coordinates.size();

		float pixel_matrix_transpose[3][N];
		for (int i = 0; i < N; ++i) {
			pixel_matrix_transpose[0][i] = static_cast<float>(pixel_coordinates[i]->x);
			pixel_matrix_transpose[1][i] = static_cast<float>(pixel_coordinates[i]->y);
			pixel_matrix_transpose[2][i] = 1.;
		}

		Mat pixel_matrix_transpose_converted = Mat(3, N, CV_32F, pixel_matrix_transpose);
		pixel_matrix_transpose_converted.convertTo(pixel_matrix_transpose_converted, CV_64F);
		Mat lonlat_matrix_transpose = config.M * pixel_matrix_transpose_converted;

		std::vector<Point2f*>* lonlat_coordinates = new std::vector<Point2f*>(N);

		for (int i = 0; i < N; ++i) {
			float scale_factor = lonlat_matrix_transpose.at<double>(i,2);
			Point2f* lonlat = new Point2f(0,0);
			lonlat->x = lonlat_matrix_transpose.at<double>(i,0) / scale_factor;
			lonlat->y = lonlat_matrix_transpose.at<double>(i,1) / scale_factor;
			(*lonlat_coordinates)[i] = lonlat;
		}

		return lonlat_coordinates;
	}

	// Convert a set of lon-lat coordinates to pixel coordinates
	std::vector<Point2f*>* lonlat_to_pixel(PixelMapperConfig &config, std::vector<Point2f*>& lonlat_coordinates) {
		int N = lonlat_coordinates.size();

		float lonlat_matrix_transpose[3][N];
		for (int i = 0; i < N; ++i) {
			lonlat_matrix_transpose[0][i] = static_cast<float>(lonlat_coordinates[i]->x);
			lonlat_matrix_transpose[1][i] = static_cast<float>(lonlat_coordinates[i]->y);
			lonlat_matrix_transpose[2][i] = 1.;
		}

		Mat lonlat_matrix_transpose_converted = Mat(3, N, CV_32F, lonlat_matrix_transpose);
		lonlat_matrix_transpose_converted.convertTo(lonlat_matrix_transpose_converted, CV_64F);
		Mat pixel_matrix_transpose = config.invM * lonlat_matrix_transpose_converted;

		std::vector<Point2f*>* pixel_coordinates = new std::vector<Point2f*>(N);

		for (int i = 0; i < N; ++i) {
			float scale_factor = pixel_matrix_transpose.at<double>(i,2);
			Point2f* pixel_coordinate = new Point2f(0,0);
			pixel_coordinate->x = pixel_matrix_transpose.at<double>(i,0) / scale_factor;
			pixel_coordinate->y = pixel_matrix_transpose.at<double>(i,1) / scale_factor;
			(*pixel_coordinates)[i] = pixel_coordinate;
		}

		return pixel_coordinates;
	}

	// Convert a set of lon-lat coordinates to 3D coordinates
	std::vector<Point3f*>* lonlat_to_3D(PixelMapperConfig &config, std::vector<Point2f*>& lonlat_coordinates) {
	  int N = lonlat_coordinates.size();

	  std::vector<Point3f*>* threeD_coordinates = new std::vector<Point3f*>(N);

	  for (int i = 0; i < N; ++i) {
		  float lon_d = lonlat_coordinates[i]->x - config.lonlat_origin[i].x;
		  float lat_d = lonlat_coordinates[i]->y - config.lonlat_origin[i].y;

		  float lon_m = lon_d * config.lon_const;
		  float lat_m = lat_d * config.lat_const;

		  Point3f* threeD_coordinate = new Point3f(0,0,0);
		  threeD_coordinate->x = lat_m;
		  threeD_coordinate->y = lon_m;
		  threeD_coordinate->z = 0;
		  (*threeD_coordinates)[i] = threeD_coordinate;
	  }
	  
	  return threeD_coordinates;
	}

	// Convert a set of 3D coordinates to lon-lat coordinates
	std::vector<Point2f*>* _3D_to_lonlat(PixelMapperConfig &config, std::vector<Point3f*>& threeD_coordinates) {
	  int N = threeD_coordinates.size();
	  float (*lonlat_coordinates_val)[2] = new float[N][2];

	  std::vector<Point2f*>* lonlat_coordinates = new std::vector<Point2f*>(N);
	  for (int i = 0; i < N; ++i) {
		  float lon_m = threeD_coordinates[i]->x;
		  float lat_m = threeD_coordinates[i]->y;

		  float lon_d = lon_m / config.lon_const;
		  float lat_d = lat_m / config.lat_const;

		  float lon_coord = lat_d + config.lonlat_origin->y;
		  float lat_coord = lon_d + config.lonlat_origin->x;

		  Point2f* lonlat_coordinate = new Point2f(0,0);
		  lonlat_coordinate->x = lat_coord;
		  lonlat_coordinate->y = lon_coord;
		  (*lonlat_coordinates)[i] = lonlat_coordinate;
	  }
	  return lonlat_coordinates;
	}

} // namespace PixelMapper

namespace CVUtils {
	int computeArea(int box[4]) {
		//TODO
		return 0;
	}
	int computeIntersection(int boxA[4], int boxB[4]) {
		//TODO
		return 0;
	}
	float computeIoU (int boxA[4], int boxB[4]) {
		//TODO
		return 0;
	}
	float computeIoA (int boxA[4], int boxB[4]) {
		//TODO
		return 0;
	}
} //namespace CVUtils

/*
namespace CVOutput {

    
	void predict(cv::Mat &image, dashboard &dash) {
		//Running image through cv model --> person_boxes, scores, classes
		//Running image through mask detector --> face_boxes, masked
		float detection_scores[];
		string detection_classes[];
		int detection_boxes[][4];

		int face_boxes[][4];
		int masked[];

		//Remainder of code is spent filling in values for distanced
		//	and whether objects are masked
		/*
		PSEUDOCODE (needs to be reworked for cpp)
		for(int i = 0 ; i < detection_boxes.size() ; i++){
			if(detection_scores[i] < 0.8)
				break;
			if(!detection_classes[i] == "person")
				continue;

			double box[] = detection_boxes[i];

			double midpoint[2] = {(box[0]+box[2])/2, box[3]};

			double long_lat[] = pm.pixel_to_lonlat(midpoint)[0];
			double coord3D[] = pm.lonlat_to_3D(long_lat);

			//0=unsure, 1=wearing, 2=not wearing
			int wearingMask = 0;

			for(int i = 0; i<face_boxes.size(); ++i){
				double face_box = face_boxes[i];
				double mask = masked[i];
				faceBoxes_subList.insert(face_box);
				boxes_subList.insert(box);
				
				double IOA = utils::computeIOA(face_box, box);
				if(IOA > 0.9){
					if(mask > 0.7)
						wearingMask = 1;
					else if(mask < 0.7)
						wearingMask = 2;
					else
						break;
				}
			}
			lat_vals.insert(long_lat[0])
			lon_vals.insert(long_lat[1])
			X3D_vals.insert(coord3D[0])
			Y3D_vals.insert(coord3D[1])
			Z3D_vals.insert(coord3D[2])
			masked.insert(wearingMask)
		}

		TrackedObject.TrackedObject.track(boxes, X3D_vals, Y3D_vals, Z3D_vals);
		map<string,int>trackedObjects = TrackedObject.TrackedObject.objects;

		for(string key : trackedObjects.keys()){
			trackedObjectsDict[key] = trackedObjects[key].toDict();
		}
		int distanced[] = 1 * sizeof(X3D_vals); //WRONG
		int X3D_vals_len = sizeof(X3D_vals);
		for(int i = 0 ; i < X3D_vals_len ; i++){
			for(int j = 0 ; j < i+1 && X3D_vals_len ; j++){ //check if this is valid
				if(distanced[i] == 0 && distanced[j] ==0){
					continue;
				}
				double distance[] = {X3D_vals[i]-X3D_vals[j], Y3D_vals[i]-Y3D_vals[j], Z3D_vals[i]-Z3D_vals[j]};
				for(int element : distance){
					distance = sqrt(arraySum(pow(element,2.0))); //IS THE SUM RIGHT?
				}
				if(distance < distance_threshold){
					distanced[i] = 0;
					distanced[j] = 0;
				}
				if 1 not in distanced{ //HOW U DO THIS ON CPP???
					break;
				}
			}
		}
		map<string,double,int> predOutput = {"X3D_vals":X3D_vals, "Y3D_vals":Y3D_vals, "Z3D_vals":Z3D_vals,
		"lat_vals":lat_vals, "lon_vals":lon_vals, "masked":masked, "distanced":distanced,
		"tracked":trackedObjectsDict};
		*/
		//return;
/*
	}

}
*/