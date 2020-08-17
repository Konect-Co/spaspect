    // Copyright 2020 The Konect SpaSpect Authors. All Rights Reserved.
// This file is part of Konect SpaSpect technology.
//  ___            ___              _   
// / __|_ __  __ _/ __|_ __  ___ __| |_ 
// \__ \ '_ \/ _` \__ \ '_ \/ -_) _|  _|
// |___/ .__/\__,_|___/ .__/\___\__|\__|
//     |_|            |_|               

#include <algorithm>

#include "CVUtils.h"
#include "Track.h"
#include "DashboardInfo.h"

using namespace std;


bool DashboardInfo::dashboard::addTrackedObject(Track::TrackedEntity* object) {
	//TODO: Add checks
	this->objects.push_back(object);
	return true;
}

bool DashboardInfo::dashboard::removeTrackedObject(Track::TrackedEntity* object) {
	int obj_pos = find(objects.begin(), objects.end(), object) - objects.begin();
	if (obj_pos != objects.size()-1) {
		objects.erase(objects.begin() + obj_pos-1);
		return true;
	}
	return false;
}

void DashboardInfo::dashboard::track(std::vector<Track::locationInfo*> newObjects) {
	Track::TrackedEntity::updateTime();

	map<Track::TrackedEntity*, vector<float>> allIOUValues;
	for (auto currentEntity : this->objects) {
		int* predictedBox = currentEntity->estimateBB();
		vector<float> IOUValues;
		for (auto newObject : newObjects) {
			float IOU = CVUtils::compute_IoU(predictedBox, newObject->boundingBox);
			IOUValues.push_back(IOU);
		}

		sort(IOUValues.begin(), IOUValues.end(), greater<float>());
		allIOUValues[currentEntity] = IOUValues;
	}
	//TODO
}

void DashboardInfo::dashboard::prune() {
	//TODO
	std::vector<Track::TrackedEntity*> to_delete;
	int updateThreshold = 5;
	
	for(auto tracked_key : this->objects){
    	int tracked_key_pos = find(this->objects.begin(), this->objects.end(), tracked_key) - this->objects.begin();
    	auto tracked = this->objects[tracked_key_pos];
    	if(Track::TrackedEntity::currTime - tracked->lastUpdate > updateThreshold){
        	to_delete.push_back(tracked_key);
    	}
	}
	for(auto delete_i : to_delete){
    	int delete_i_pos = find(this->objects.begin(), this->objects.end(), delete_i)- this->objects.begin();
    	this->objects.erase(this->objects.begin() + delete_i_pos-1);
	}
};