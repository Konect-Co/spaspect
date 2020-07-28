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
#include "TrackedObject.h"
#inlcude "tensorflow/tensorflow/cc/saved_model/loader.h"

using namespace std;

namespace DashboardInfo {
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
	public:

	
		string streamlink;
		string name;
		std::vector<Track::TrackedEntity*> objects;

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
			int obj_pos = std::find(objects.begin(), objects.end(), object) - objects.begin();
			if (obj_pos != objects.end()) {
				objects.erase(obj_pos);
				return true;
			}
			return false;
		}
	}

} //namespace DashboardInfo

namespace PixelMapper {
	class PixelMapperConfig {
	public:
		int pixel_array[4][2];
		int lonlat_array[4][2];

		int lonlat_origin[2];

		float lon_const;
		float lat_const = 111320;

		PixelMapperConfig(int &pixel_array[4][2], int &lonlat_array[4][2], int &lonlat_origin[2]) : 
			pixel_array(pixel_array), lonlat_array(lonlat_array), lonlat_origin(lonlat_origin){
			lon_const = 40075000 * cos(lonlat_origin[0]*M_PI/180) / 360;
		}
	}

	//	Convert a set of pixel coordinates to lon-lat coordinates
	int[][2] pixel_to_lonlat(PixelMapperConfig &config, int[][2] pixel_coordinates) {
		//TODO
		return;
	}

	// Convert a set of lon-lat coordinates to pixel coordinates
	int[][2] lonlat_to_pixel(PixelMapperConfig &config, int[][2] lonlat_coordinates) {
		//TODO
		return;
	}

	// Convert a set of lon-lat coordinates to 3D coordinates
	int[][3] lonlat_to_3D(PixelMapperConfig &config, int[][2] lonlat_coordinates) {
		//TODO
		return;
	}

	// Convert a set of 3D coordinates to lon-lat coordinates
	int[][2] _3D_to_lonlat(PixelMapperConfig &config, int[][3] _3D_coordinates) {
		//TODO
		return;
	}

} //namespace PixelMapper

namespace CVOutput {
	namespace utils {
		int computeArea(int box[4]) {
			//TODO
			return 0;
		}
		int computeIntersection(int boxA[4], int boxB[4]) {
			//TODO
			return 0;
		}
		int computeIoU (int boxA[4], int boxB[4]) {
			//TODO
			return 0;
		}
		int computeIoA (int boxA[4], int boxB[4]) {
			//TODO
			return 0;
		}
	} //namespace utils
    
	void predict(cv::Mat &image, dashboard &dash) {
		//Running image through cv model --> person_boxes, scores, classes
		    
        string model_dir = "/home/santript/ImportantProjects/spaspect/core/cv_model/models/mobilenet-model";
        tensorflow::SavedModelBundle model;
        auto status = tensorflow::LoadSavedModel(session_options, run_options, model_dir, {tensorflow::kSavedModelTagServe}, &model);
        if (!status.ok()) {
            cerr << "Failed: " << status;
            return;
        }
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
		return;
	}
}

namespace Track {
	class TrackedEntity {
	public:
		float lastUpdate;
		float velocity[2];
		std::map<int, locationInfo> history;
		void addNext(float time, locationInfo &newLocationInfo) {
			history[time] = newLocationInfo;
			// TODO: Update velocity
		}
		//Computes the prediction of the next bounding box using velocity and current position
		int[4] estimateBB() {
			//TODO
		}
	};

	float time;

	void updateTime() {
		//TODO
	}

	void track(dashboard &dash, std::vector<DashboardInfo::locationInfo*>) {
		//TODO
	}

	void prune(dashboard &dash) {
		//TODO
	}
} //namespace Track