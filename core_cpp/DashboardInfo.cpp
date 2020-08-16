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
};