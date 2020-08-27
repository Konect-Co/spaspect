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

#include "Track.h"

using namespace std;

namespace DashboardInfo {
	struct calibration {
		float lon_vals[4];
		float lat_vals[4];			
		float lonlat_origin[2];
		int pixelX_vals[4];
		int pixelY_vals[4];
	};

	//Data structure that represents the dashboard
	class dashboard {
	public:
		string streamlink;
		string name;
		vector<Track::TrackedEntity*> objects;

		struct calibration dash_calib;

		dashboard(string streamlink, string name, vector<Track::TrackedEntity*>* objects_ptr, struct calibration dash_calib) : 
			streamlink(streamlink), name(name), objects(*objects_ptr), dash_calib(dash_calib) {}

		bool add_tracked_object(Track::TrackedEntity* object);
		bool remove_tracked_object(Track::TrackedEntity* object);

		void track(Track::TrackedEntity* object, std::vector<Track::locationInfo*> newObjects);
	};
} //namespace DashboardInfo