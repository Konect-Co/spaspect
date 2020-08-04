// Copyright 2020 The Konect SpaSpect Authors. All Rights Reserved.
// This file is part of Konect SpaSpect technology.
//  ___            ___              _   
// / __|_ __  __ _/ __|_ __  ___ __| |_ 
// \__ \ '_ \/ _` \__ \ '_ \/ -_) _|  _|
// |___/ .__/\__,_|___/ .__/\___\__|\__|
//     |_|            |_|               


#include <iostream>
#include <string>
#include <opencv2/opencv.hpp>
#include <opencv2/core/core.hpp>

#include "utils.h"

using namespace std;

int main() {
	cv::Mat* image;

	for (;;) {
		cv::VideoCapture cap("/home/ravit/Downloads/TimesSquare.mp4");
		cap >> (*image);

		if(! image->data ) {
			return -1;
		}
	}

	return 0;
}