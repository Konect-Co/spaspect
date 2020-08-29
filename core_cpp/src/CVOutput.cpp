// Copyright 2020 The Konect SpaSpect Authors. All Rights Reserved.
// This file is part of Konect SpaSpect technology.
//  ___            ___              _   
// / __|_ __  __ _/ __|_ __  ___ __| |_ 
// \__ \ '_ \/ _` \__ \ '_ \/ -_) _|  _|
// |___/ .__/\__,_|___/ .__/\___\__|\__|
//     |_|            |_|               

#include <vector>
#include <algorithm>
#include <string>
#include <opencv2/opencv.hpp>
#include <iterator>
#include <map>
#include <iostream>
#include <algorithm>

#include "CVOutput.h"
#include "CVUtils.h"
#include "PixelMapper.h"
#include "DashboardInfo.h"

using namespace std;
using namespace cv;

void CVOutput::predict(Mat &image, DashboardInfo::dashboard &dash, int distance_threshold = 2) {
	//Running image through cv model --> person_boxes, scores, classes
	//Running image through mask detector --> face_boxes, masked
	vector<float> detection_scores;
	vector<string> detection_classes;
	vector<int> detection_boxes;
    
    vector<int> face_boxes;
    vector<float> lat_vals;
	vector<float> lon_vals;
	vector<float> X3D_vals;
	vector<float> Y3D_vals;
	vector<float> Z3D_vals;
	vector<int> masked;
    
    
	//Remainder of code is spent filling in values for distanced
	//	and whether objects are masked
	
	for(int i = 0 ; i < detection_boxes.size() ; i++){
		if(detection_scores.at(i) < 0.8)
			break;
		if(detection_classes.at(i) != "person")
			continue;

		vector<float> box;
		box.push_back(detection_boxes.at(i));

		double midpoint[2] = {(box[0]+box[2])/2, box[3]};

		vector<double> long_lat = pm.pixel_to_lonlat(midpoint)[0];
		vector<double> coord3D = pm.lonlat_to_3D(long_lat);

		//0=unsure, 1=wearing, 2=not wearing
		int wearingMask = 0;
		vector<float> faceBoxes_subList;
		vector<float> boxes_subList;

		for(int i = 0; i<face_boxes.size(); ++i){
			double face_box = face_boxes.at(i);
			double mask = masked.at(i);
			faceBoxes_subList.push_back(face_box);
			boxes_subList.push_back(box);
			
			double IOA = CVUtils::compute_IoA(face_box, box);
			if(IOA > 0.9){
				if(mask > 0.7)
					wearingMask = 1;
				else if(mask < 0.7)
					wearingMask = 2;
				else
					break;
			}
		}
		
		
		lat_vals.push_back(long_lat.at(0));
		lon_vals.push_back(long_lat.at(1));
		X3D_vals.push_back(coord3D.at(0));
		Y3D_vals.push_back(coord3D.at(1));
		Z3D_vals.push_back(coord3D.at(2));
		masked.push_back(wearingMask);
	}

	DashboardInfo::dashboard::track(boxes, X3D_vals, Y3D_vals, Z3D_vals); //wrong num of params
	map<string,int> trackedObjects = TrackedObject.TrackedObject.objects;
	vector<string> keys;

	for(map<string,int>::iterator it = trackedObjects.begin(); it != trackedObjects.end(); ++it){
		keys.push_back(it->first);
	}

	for(string key : keys){
		trackedObjectsDict[key] = trackedObjects[key].toDict(); //line 64 utils.py
	}
	int distanced[] = 1 * X3D_vals.size(); //WRONG
	int X3D_vals_len = X3D_vals.size();
	for(int i = 0 ; i < X3D_vals_len ; i++){
		for(int j = 0 ; j < i+1 && X3D_vals_len ; j++){ //check if this is valid
			if(distanced[i] == 0 && distanced[j] ==0){
				continue;
			}
			double distance[] = {X3D_vals[i]-X3D_vals[j], Y3D_vals[i]-Y3D_vals[j], Z3D_vals[i]-Z3D_vals[j]};
			for(int element : distance){
				distance = sqrt(arraySum(pow(element,2.0))); //IS THE SUM RIGHT?
			}
			if(*distance < distance_threshold){
				distanced[i] = 0;
				distanced[j] = 0;
			}

			for(int x = 0 ; x < sizeof(distanced)/sizeof(distanced[0]) ; x++){
    			if(distanced[x] != 1){
        			break;
    			}
			}
		}
	}
	map<string,vector<float>,vector<int>> predOutput; //FIX THIS


	predOutput["X3D_vals"] = X3D_vals;
	predOutput["Y3D_vals"] = Y3D_vals;
	predOutput["Z3D_vals"] = Z3D_vals;
	predOutput["lat_vals"] = lat_vals;
	predOutput["lon_vals"] = lon_vals;
	predOutput["masked"] = masked;
	predOutput["distanced"] = distanced;
	predOutput["tracked"] = trackedObjectsDict;

/*
	predOutput.insert(std::make_pair("X3D_vals", X3D_vals));
	predOutput.insert(std::make_pair("Y3D_vals", Y3D_vals));
	predOutput.insert(std::make_pair("Z3D_vals", Z3D_vals));
	predOutput.insert(std::make_pair("lat_vals", lat_vals));
	predOutput.insert(std::make_pair("lon_vals", lon_vals));
	predOutput.insert(std::make_pair("masked", masked));
	predOutput.insert(std::make_pair("distanced", distanced));
	predOutput.insert(std::make_pair("tracked", tracked));
*/
/*
	predOutput.insert(pair<string,double>("X3D_vals",X3D_vals));
	predOutput.insert(pair<string,double>("Y3D_vals",Y3D_vals));
	predOutput.insert(pair<string,double>("Z3D_vals",Z3D_vals));
	predOutput.insert(pair<string,double>("lat_vals",lat_vals));
	predOutput.insert(pair<string,double>("lon_vals",lon_vals));
	predOutput.insert(pair<string,int>("masked",masked));
	predOutput.insert(pair<string,int>("distanced",distanced));
	predOutput.insert(pair<string,double>("tracked",trackedObjectsDict));
*/
	//return;
}