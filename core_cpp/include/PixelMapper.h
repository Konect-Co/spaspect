// Copyright 2020 The Konect SpaSpect Authors. All Rights Reserved.
// This file is part of Konect SpaSpect technology.
//  ___            ___              _   
// / __|_ __  __ _/ __|_ __  ___ __| |_ 
// \__ \ '_ \/ _` \__ \ '_ \/ -_) _|  _|
// |___/ .__/\__,_|___/ .__/\___\__|\__|
//     |_|            |_|               
#include <iostream>
#include <string>
#include <cmath>
#include <cassert>
#include <array>
#include <algorithm>
#include <vector>

#include <opencv2/opencv.hpp>
#include <opencv2/core/types.hpp>
#include "NumCpp.hpp"

using namespace std;
using namespace cv;

namespace PixelMapper {
	class PixelMapperConfig {
	public:
	  Point2f pixel_array[4];
	  Point2f lonlat_array[4];

	  Point2f* lonlat_origin;

	  float lat_const;
	  float lon_const;

	  Mat M;
	  Mat invM;
	  
	PixelMapperConfig(Point2f (&pixel_array)[4], Point2f (&lonlat_array)[4], Point2f* (&lonlat_origin))
	  : lonlat_origin(lonlat_origin) {
	  	this->lat_const = 111320.;
	    this->lon_const = 40075000 * cos(lonlat_origin->x * M_PI / 180) / 360;

	    this->pixel_array[0] = pixel_array[0];
	    this->pixel_array[1] = pixel_array[1];
	    this->pixel_array[2] = pixel_array[2];
	    this->pixel_array[3] = pixel_array[3];

	    this->lonlat_array[0] = lonlat_array[0];
	    this->lonlat_array[1] = lonlat_array[1];
	    this->lonlat_array[2] = lonlat_array[2];
	    this->lonlat_array[3] = lonlat_array[3];

		this->M = getPerspectiveTransform(pixel_array, lonlat_array);
		this->invM = getPerspectiveTransform(lonlat_array, pixel_array);
	  }
	};

	// Convert a set of pixel coordinates to lon-lat coordinates
	std::vector<Point2f*>* pixel_to_lonlat(PixelMapperConfig &config, std::vector<Point2f*>& pixel_coordinates);

	// Convert a set of lon-lat coordinates to pixel coordinates
	std::vector<Point2f*>* lonlat_to_pixel(PixelMapperConfig &config, std::vector<Point2f*>& lonlat_coordinates);

	// Convert a set of lon-lat coordinates to 3D coordinates
	std::vector<Point3f*>* lonlat_to_3D(PixelMapperConfig &config, std::vector<Point2f*>& lonlat_coordinates);

	// Convert a set of 3D coordinates to lon-lat coordinates
	std::vector<Point2f*>* _3D_to_lonlat(PixelMapperConfig &config, std::vector<Point3f*>& threeD_coordinates);

} // namespace PixelMapper