// Copyright 2020 The Konect SpaSpect Authors. All Rights Reserved.
// This file is part of Konect SpaSpect technology.
//  ___            ___              _   
// / __|_ __  __ _/ __|_ __  ___ __| |_ 
// \__ \ '_ \/ _` \__ \ '_ \/ -_) _|  _|
// |___/ .__/\__,_|___/ .__/\___\__|\__|
//     |_|            |_|               
#pragma once

#include <map>
#include <ctime>
#include <vector>

using namespace std;

namespace Track {
	//Data structure that location and pixel bounding box information
	struct locationInfo {
		int boundingBox[4];
		int _3DCoordinate[3];
		int lonlatCoordinate[2];
	};

	//Data structure that stores information about the object
	struct entityInfo {
		struct locationInfo location;
		bool distanced;
		bool masked;
	};
	class TrackedEntity {
	public:
		float currTime;

		float lastUpdate;
		float velocity[2];
		map<int, locationInfo> history;

		TrackedEntity():lastUpdate(currTime), velocity{0, 0}, history(std::map<int, locationInfo>()) {}

		void addNext(locationInfo &newLocationInfo);

		int* estimateBB();
		void updateTime();
	};
}; // namespace Track