// Copyright 2020 The Konect SpaSpect Authors. All Rights Reserved.
// This file is part of Konect SpaSpect technology.
//  ___            ___              _   
// / __|_ __  __ _/ __|_ __  ___ __| |_ 
// \__ \ '_ \/ _` \__ \ '_ \/ -_) _|  _|
// |___/ .__/\__,_|___/ .__/\___\__|\__|
//     |_|            |_|               
#pragma once

#include <map>
//#include "DashboardInfo.h"

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
		static float currTime;

		float lastUpdate;
		float velocity[2];
		map<int, locationInfo> history;

		TrackedEntity():lastUpdate(currTime), velocity{0, 0}, history(std::map<int, locationInfo>()) {}

		void addNext(float time, locationInfo &newLocationInfo) {
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

		int* estimateBB() {
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

		class dashboard;
		static void track(dashboard* dash, std::vector<locationInfo*>) {
			//TODO
		}

		static void prune(dashboard* dash) {
			//TODO
		}
	};
} // namespace Track