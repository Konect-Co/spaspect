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
	//Data structure that represents the dashboard
	class dashboard {
	public:
		string streamlink;
		string name;
		vector<Track::TrackedEntity*> objects;

		class {
		public:
			float lon_vals[4];
			float lat_vals[4];			
			float lonlat_origin[2];
			int pixelX_vals[4];
			int pixelY_vals[4];
		} calibration;

		bool addTrackedObject(Track::TrackedEntity* object);
		bool removeTrackedObject(Track::TrackedEntity* object);

		void track(std::vector<Track::locationInfo*> objects);
		void prune();
	};
} //namespace DashboardInfo