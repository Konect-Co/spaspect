// Copyright 2020 The Konect SpaSpect Authors. All Rights Reserved.
//
// This file is part of Konect SpaSpect technology.

#include <iostream>
#include <string>
#include <opencv2/opencv.hpp>
#include <opencv2/core/core.hpp>

#include "PixelMapper.h"
#include "TrackedObject.h"
#include "utils.h"

using namespace std;

int main() {
	cv::Mat image;

	cv::VideoCapture cap("/home/ravit/Downloads/TimesSquare.mp4");
	cap >> image;

	if(! image.data )
	{
		cout <<  "Could not open or find the image" << std::endl;
		return -1;
	} else {
		cout << "Opened image" << std::endl;
		cv::imwrite("/home/ravit/Pictures/output.png", image);
	}

	return 0;
}