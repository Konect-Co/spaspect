// Copyright 2020 The Konect SpaSpect Authors. All Rights Reserved.
// This file is part of Konect SpaSpect technology.
//  ___            ___              _   
// / __|_ __  __ _/ __|_ __  ___ __| |_ 
// \__ \ '_ \/ _` \__ \ '_ \/ -_) _|  _|
// |___/ .__/\__,_|___/ .__/\___\__|\__|
//     |_|            |_|               

#include "Track.h"
//#include "DashboardInfo.h"

using namespace std;
using namespace Track;

void Track::TrackedEntity::addNext(float time, Track::locationInfo &newLocationInfo) {
	locationInfo& currLocationInfo = history[history.rbegin()->first];
	history[time] = newLocationInfo;

	//update velocity
	int newBoxCenter[2] = {static_cast<int>(newLocationInfo.boundingBox[0] + newLocationInfo.boundingBox[2]/2.), 
		static_cast<int>(newLocationInfo.boundingBox[1] + newLocationInfo.boundingBox[3]/2.)};
	int currBoxCenter[2] = {static_cast<int>(currLocationInfo.boundingBox[0] + currLocationInfo.boundingBox[2]/2.), 
		static_cast<int>(currLocationInfo.boundingBox[1] + currLocationInfo.boundingBox[3]/2.)};

	velocity[0] = static_cast<int>((newBoxCenter[0]-currBoxCenter[0]*1.) / (currTime-lastUpdate));
	velocity[1] = static_cast<int>((newBoxCenter[1]-currBoxCenter[1]*1.) / (currTime-lastUpdate));
}

//Computes the prediction of the next bounding box using velocity and current position
int* Track::TrackedEntity::estimateBB() {
	float timeDiff = currTime - lastUpdate;
	int deltaX = static_cast<int>(velocity[0]*timeDiff);
	int deltaY = static_cast<int>(velocity[1]*timeDiff);

	int* currBB = history[history.size()-1].boundingBox;
	int* newBB = new int[4];
	newBB[0] = currBB[0]+deltaX;
	newBB[1] = currBB[1]+deltaY;
	newBB[2] = currBB[2]+deltaX;
	newBB[3] = currBB[3]+deltaY;

	return newBB;
}

static void Track::TrackedEntity::updateTime() {
	currTime = std::time(0);
}

class dashboard;
static void Track::TrackedEntity::track(dashboard* dash, std::vector<Track::locationInfo*>) {
	updateTime();

	std::map<string, locationInfo> allIOUValues();
	for (auto name : dash->objects) {
		TrackedEntity currentEntity = dash->objects[name]
		int predictedBox[4] = currentEntity.estimateBB();
		std::map<int*, float> IOUValues();
		for (int box_i = 0; box_i < boundingBoxes; box_i++) {
			int IOU = computeIOU(predictedBox, boundingBoxes[box_i])
			IOUValues[box_i] = IOU
		}

		IOUValues = {k : v for k, v in sorted(IOUValues.items(), reverse=True, key = lambda kv:kv[1])}
		allIOUValues[currentEntity] = IOUValues;
		
	}
	//TODO
}

static void Track::TrackedEntity::prune(dashboard* dash) {
	//TODO
};