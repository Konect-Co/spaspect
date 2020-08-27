// Copyright 2020 The Konect SpaSpect Authors. All Rights Reserved.
// This file is part of Konect SpaSpect technology.
//  ___            ___              _   
// / __|_ __  __ _/ __|_ __  ___ __| |_ 
// \__ \ '_ \/ _` \__ \ '_ \/ -_) _|  _|
// |___/ .__/\__,_|___/ .__/\___\__|\__|
//     |_|            |_|               

#include <cppunit/extensions/HelperMacros.h>

//both must be imported due to mutual dependencies
//TODO: not optimal structure --> should be changed
#include "Track.h"
#include "DashboardInfo.h"

using namespace std;
using namespace cv;
using namespace DashboardInfo;

class DashboardInfoTest : public CPPUNIT_NS::TestFixture
{
  CPPUNIT_TEST_SUITE( DashboardInfoTest );
  CPPUNIT_TEST( test_accessing_elements );
  CPPUNIT_TEST( test_add_tracked_object );
  CPPUNIT_TEST( test_remove_tracked_object );
  CPPUNIT_TEST( test_track );
  CPPUNIT_TEST_SUITE_END();

  struct calibration mycalib;
  dashboard* test_dashboard;
  Track::TrackedEntity* object;
public:
  void setUp() {
    cout << endl << "[INFO] Performing test setup" << endl;
    test_dashboard = new dashboard("https://cdn-001.whatsupcams.com/hls/hr_selce1.m3u8", "Croatia", 
    	new vector<Track::TrackedEntity*>(), mycalib);
   	object = new Track::TrackedEntity();
  };

protected:
  void test_accessing_elements(){
  	string expected_name = "Croatia";
  	string expected_streamlink = "https://cdn-001.whatsupcams.com/hls/hr_selce1.m3u8";

  	CPPUNIT_ASSERT_EQUAL(test_dashboard->name, expected_name);
  	CPPUNIT_ASSERT_EQUAL(test_dashboard->streamlink, expected_streamlink);
  }
  void test_add_tracked_object(){
  	test_dashboard->add_tracked_object(object);
  }
  void test_remove_tracked_object(){
  	test_dashboard->remove_tracked_object(object);
  }
  void test_track(){}
};
