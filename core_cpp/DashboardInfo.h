// Copyright 2020 The Konect SpaSpect Authors. All Rights Reserved.
// This file is part of Konect SpaSpect technology.
//  ___            ___              _   
// / __|_ __  __ _/ __|_ __  ___ __| |_ 
// \__ \ '_ \/ _` \__ \ '_ \/ -_) _|  _|
// |___/ .__/\__,_|___/ .__/\___\__|\__|
//     |_|            |_|               
#pragma once

#include <iostream>
#include <vector>
#include <algorithm>

using namespace std;

namespace DashboardInfo {
	//forward declaration
	class TrackedEntity;

	//Data structure that represents the dashboard
	class dashboard {
	public:
		string streamlink;
		string name;
		vector<TrackedEntity*> objects;

		class {
		public:
			float lon_vals[4];
			float lat_vals[4];			
			float lonlat_origin[2];
			int pixelX_vals[4];
			int pixelY_vals[4];
		} calibration;

		bool addTrackedObject(TrackedEntity* object) {
			//TODO: Add checks
			this->objects.push_back(object);
			return true;
		}

		bool removeTrackedObject(TrackedEntity* object) {
			int obj_pos = find(objects.begin(), objects.end(), object) - objects.begin();
			if (obj_pos != objects.size()-1) {
				objects.erase(objects.begin() + obj_pos-1);
				return true;
			}
			return false;
		}
	};
} //namespace DashboardInfo