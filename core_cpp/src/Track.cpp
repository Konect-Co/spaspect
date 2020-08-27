// Copyright 2020 The Konect SpaSpect Authors. All Rights Reserved.
// This file is part of Konect SpaSpect technology.
//  ___            ___              _   
// / __|_ __  __ _/ __|_ __  ___ __| |_ 
// \__ \ '_ \/ _` \__ \ '_ \/ -_) _|  _|
// |___/ .__/\__,_|___/ .__/\___\__|\__|
//     |_|            |_|               

#include "Track.h"
#include "DashboardInfo.h"

using namespace std;

void Track::TrackedEntity::addNext(Track::locationInfo &newLocationInfo) {
	locationInfo& currLocationInfo = history[history.rbegin()->first];
	history[currTime] = newLocationInfo;

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

void Track::TrackedEntity::updateTime() {
	currTime = std::time(0);
}