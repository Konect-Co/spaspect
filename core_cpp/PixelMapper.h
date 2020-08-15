// Copyright 2020 The Konect SpaSpect Authors. All Rights Reserved.
// This file is part of Konect SpaSpect technology.
//  ___            ___              _   
// / __|_ __  __ _/ __|_ __  ___ __| |_ 
// \__ \ '_ \/ _` \__ \ '_ \/ -_) _|  _|
// |___/ .__/\__,_|___/ .__/\___\__|\__|
//     |_|            |_|               
#pragma once

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
	std::vector<Point2f*>* pixel_to_lonlat(PixelMapperConfig &config, std::vector<Point2f*>& pixel_coordinates) {
		int N = pixel_coordinates.size();

		float pixel_matrix_transpose[3][N];
		for (int i = 0; i < N; ++i) {
			pixel_matrix_transpose[0][i] = static_cast<float>(pixel_coordinates[i]->x);
			pixel_matrix_transpose[1][i] = static_cast<float>(pixel_coordinates[i]->y);
			pixel_matrix_transpose[2][i] = 1.;
		}

		Mat pixel_matrix_transpose_converted = Mat(3, N, CV_32F, pixel_matrix_transpose);
		pixel_matrix_transpose_converted.convertTo(pixel_matrix_transpose_converted, CV_64F);
		Mat lonlat_matrix_transpose = config.M * pixel_matrix_transpose_converted;

		std::vector<Point2f*>* lonlat_coordinates = new std::vector<Point2f*>(N);

		for (int i = 0; i < N; ++i) {
			float scale_factor = lonlat_matrix_transpose.at<double>(i,2);
			Point2f* lonlat = new Point2f(0,0);
			lonlat->x = lonlat_matrix_transpose.at<double>(i,0) / scale_factor;
			lonlat->y = lonlat_matrix_transpose.at<double>(i,1) / scale_factor;
			(*lonlat_coordinates)[i] = lonlat;
		}

		return lonlat_coordinates;
	}

	// Convert a set of lon-lat coordinates to pixel coordinates
	std::vector<Point2f*>* lonlat_to_pixel(PixelMapperConfig &config, std::vector<Point2f*>& lonlat_coordinates) {
		int N = lonlat_coordinates.size();

		float lonlat_matrix_transpose[3][N];
		for (int i = 0; i < N; ++i) {
			lonlat_matrix_transpose[0][i] = static_cast<float>(lonlat_coordinates[i]->x);
			lonlat_matrix_transpose[1][i] = static_cast<float>(lonlat_coordinates[i]->y);
			lonlat_matrix_transpose[2][i] = 1.;
		}

		Mat lonlat_matrix_transpose_converted = Mat(3, N, CV_32F, lonlat_matrix_transpose);
		lonlat_matrix_transpose_converted.convertTo(lonlat_matrix_transpose_converted, CV_64F);
		Mat pixel_matrix_transpose = config.invM * lonlat_matrix_transpose_converted;

		std::vector<Point2f*>* pixel_coordinates = new std::vector<Point2f*>(N);

		for (int i = 0; i < N; ++i) {
			float scale_factor = pixel_matrix_transpose.at<double>(i,2);
			Point2f* pixel_coordinate = new Point2f(0,0);
			pixel_coordinate->x = pixel_matrix_transpose.at<double>(i,0) / scale_factor;
			pixel_coordinate->y = pixel_matrix_transpose.at<double>(i,1) / scale_factor;
			(*pixel_coordinates)[i] = pixel_coordinate;
		}

		return pixel_coordinates;
	}

	// Convert a set of lon-lat coordinates to 3D coordinates
	std::vector<Point3f*>* lonlat_to_3D(PixelMapperConfig &config, std::vector<Point2f*>& lonlat_coordinates) {
	  int N = lonlat_coordinates.size();
  
      std::vector<Point3f*>* threeD_coordinates = new std::vector<Point3f*>(N);

      for (int i = 0; i < N; ++i) {
        	float lon_d = lonlat_coordinates[i]->x - config.lonlat_origin[i].x;
    		float lat_d = lonlat_coordinates[i]->y - config.lonlat_origin[i].y;
    
    		float lon_m = lon_d * config.lon_const;
    		float lat_m = lat_d * config.lat_const;

    		Point3f* threeD_coordinate = new Point3f(0,0,0);
    		threeD_coordinate->x = lat_m;
    		threeD_coordinate->y = lon_m;
    		threeD_coordinate->z = 0;
    		(*threeD_coordinates)[i] = threeD_coordinate;
    	  }
	  
    	  return threeD_coordinates;
	}

	// Convert a set of 3D coordinates to lon-lat coordinates
	std::vector<Point2f*>* _3D_to_lonlat(PixelMapperConfig &config, std::vector<Point3f*>& threeD_coordinates) {
	  int N = threeD_coordinates.size();
	  float (*lonlat_coordinates_val)[2] = new float[N][2];

	  std::vector<Point2f*>* lonlat_coordinates = new std::vector<Point2f*>(N);
	  for (int i = 0; i < N; ++i) {
		  float lon_m = threeD_coordinates[i]->x;
		  float lat_m = threeD_coordinates[i]->y;

		  float lon_d = lon_m / config.lon_const;
		  float lat_d = lat_m / config.lat_const;

		  float lon_coord = lat_d + config.lonlat_origin->y;
		  float lat_coord = lon_d + config.lonlat_origin->x;

		  Point2f* lonlat_coordinate = new Point2f(0,0);
		  lonlat_coordinate->x = lat_coord;
		  lonlat_coordinate->y = lon_coord;
		  (*lonlat_coordinates)[i] = lonlat_coordinate;
	  }
	  return lonlat_coordinates;
	}
} // namespace PixelMapper