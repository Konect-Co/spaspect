// Copyright 2020 The Konect SpaSpect Authors. All Rights Reserved.
// This file is part of Konect SpaSpect technology.
//  ___            ___              _   
// / __|_ __  __ _/ __|_ __  ___ __| |_ 
// \__ \ '_ \/ _` \__ \ '_ \/ -_) _|  _|
// |___/ .__/\__,_|___/ .__/\___\__|\__|
//     |_|            |_|               
#pragma once

namespace CVUtils {
	int compute_area(int box[4]) {
		//TODO
		int box_reformed[4] = {box[0], box[1], box[0]+box[2], box[1]+box[3]};
		int area = (box_reformed[2]-box_reformed[0])*(box_reformed[3]-box_reformed[1]);
		return area;
    }
	int compute_intersection(int boxA[4], int boxB[4]) {
		//TODO
		int intersection;
		int boxA_reformed[4] = {boxA[0], boxA[1], boxA[0]+boxA[2], boxA[1]+boxA[3]};
		int boxB_reformed[4] = {boxB[0], boxB[1], boxB[0]+boxB[2], boxB[1]+boxB[3]};
		
		if(boxB_reformed[0] > boxA_reformed[2] || boxA_reformed[0] > boxB_reformed[2] || boxB_reformed[1] > boxA_reformed[3] || boxA_reformed[1] > boxB_reformed[3]){
    		return 0;
		}
		int xVals[4] = {boxA_reformed[0], boxA_reformed[2], boxB_reformed[0], boxB_reformed[2]};
		int yVals[4] = {boxA_reformed[1], boxA_reformed[3], boxB_reformed[1], boxB_reformed[3]};
		
		std::sort(xVals, xVals+4);
		std::sort(yVals, yVals+4);
		
		intersection = (xVals[2]-xVals[1])*(yVals[2]-yVals[1]);
		
		return intersection;
    }
	float compute_IoU (int boxA[4], int boxB[4]) {
		//TODO
		float intersection = compute_intersection(boxA,boxB);
		float the_union = compute_area(boxA) + compute_area(boxB) - intersection;
		
		float iou = intersection / the_union;
		
		return iou;
    }
	float compute_IoA (int boxA[4], int boxB[4]) {
		//TODO
		float intersection = compute_intersection(boxA,boxB);
		float aArea = compute_area(boxA);
		
		float iou = intersection / aArea;
		
		return iou;
    }
} //namespace CVUtils