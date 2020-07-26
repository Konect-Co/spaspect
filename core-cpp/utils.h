#pragma once
#include <"TrackedObject.h">
#include <map>
#include <iostream>
#include <string>
//add to opencv2
#include <opencv2/opencv.hpp>
using namespace std;

map<string, int>
map<string,int> makeVisualizationOutput(map<string,int> CVOutput,map<string,int> CVOutput, int distance_threshhold=2, float score_threshold = 0.60){
    double X3D_vals[] = {};
    double Y3D_vals[] = {};
    double Z3D_vals[] = {};
    double lat_vals[] = {};
    double lon_vals[] = {};
    
    int masked[] = {};
    double boxes[] = {};
    
    int db_len = sizeof(CVOutput["detection_boxes"]);
    for(int i = 0 ; i < db_len ; i++){
        if(CVOutput["detection_scores"][i] < score_threshold){
            break;
        }
        if(!CVOutput["detection_classes"][i] == "person"){
            continue;
        }
        
        double box[] = CVOutput["detection_boxes"][i];
        boxes.insert(box);
        
        double midpoint[] = {int((box[0]+box[2])/2), box[3]};
        
        double long_lat[] = pm.pixel_to_lonlat(midpoint)[0];
        double coord3D[] = pm.lonlat_to_3D(long_lat);
        
        //0=unsure, 1=wearing, 2=not wearing
        int wearingMask = 0;
        double faceBoxes_subList[] = {};
        double boxes_subList[] = {};
        
        for(int maskOut : CVOutput["masks"]){
            double face_box = maskOut[0];
            double mask = maskOut[1];
            faceBoxes_subList.insert(face_box);
            boxes_subList.insert(box);
            double IOA = cv_utils.computeIOA(face_box, box); //THIS PART IS UNDEFINED
            if(IOA > 0.9){
                if(mask > 0.7){
                    wearingMask = 1;
                }
                else if(mask < 0.7){
                    wearingMask = 2;
                }
                else{
                    break;
                }
            }
        }
        lat_vals.insert(long_lat[0])
		lon_vals.insert(long_lat[1])
		X3D_vals.insert(coord3D[0])
		Y3D_vals.insert(coord3D[1])
		Z3D_vals.insert(coord3D[2])
		masked.insert(wearingMask)
        
    }
    	TrackedObject.TrackedObject.track(boxes, X3D_vals, Y3D_vals, Z3D_vals) //I THINK IT'S UNDEFINED?
    	map<string,int>trackedObjects = TrackedObject.TrackedObject.objects; //NOT RIGHT
    	map<string,int>trackedObjectsDict; //WRONG
    	
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
		
		return predOutput;
}