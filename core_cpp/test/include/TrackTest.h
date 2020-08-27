// Copyright 2020 The Konect SpaSpect Authors. All Rights Reserved.
// This file is part of Konect SpaSpect technology.
//  ___            ___              _   
// / __|_ __  __ _/ __|_ __  ___ __| |_ 
// \__ \ '_ \/ _` \__ \ '_ \/ -_) _|  _|
// |___/ .__/\__,_|___/ .__/\___\__|\__|
//     |_|            |_|               

#include <cppunit/extensions/HelperMacros.h>
#include "Track.h"
#include "DashboardInfo.h"

using namespace std;
using namespace cv;
using namespace Track;

class TrackTest : public CPPUNIT_NS::TestFixture
{
  CPPUNIT_TEST_SUITE( TrackTest );
  CPPUNIT_TEST( test_pixel_to_lonlat );
  CPPUNIT_TEST_SUITE_END();

protected:
  //any needed variables

public:
  void setUp() {
    cout << endl << "[INFO] Performing test setup" << endl;
  };

protected:
  void test_pixel_to_lonlat(){}
};
