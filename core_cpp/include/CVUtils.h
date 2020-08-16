// Copyright 2020 The Konect SpaSpect Authors. All Rights Reserved.
// This file is part of Konect SpaSpect technology.
//  ___            ___              _   
// / __|_ __  __ _/ __|_ __  ___ __| |_ 
// \__ \ '_ \/ _` \__ \ '_ \/ -_) _|  _|
// |___/ .__/\__,_|___/ .__/\___\__|\__|
//     |_|            |_|               
#pragma once

#include <algorithm>

namespace CVUtils {
	int compute_area(int box[4]);
	int compute_intersection(int boxA[4], int boxB[4]);
	float compute_IoU (int boxA[4], int boxB[4]);
	float compute_IoA (int boxA[4], int boxB[4]);
} //namespace CVUtils