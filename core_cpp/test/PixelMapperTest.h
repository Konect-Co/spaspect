// Copyright 2020 The Konect SpaSpect Authors. All Rights Reserved.
// This file is part of Konect SpaSpect technology.
//  ___            ___              _   
// / __|_ __  __ _/ __|_ __  ___ __| |_ 
// \__ \ '_ \/ _` \__ \ '_ \/ -_) _|  _|
// |___/ .__/\__,_|___/ .__/\___\__|\__|
//     |_|            |_|               

#include <cppunit/extensions/HelperMacros.h>
#include "../utils.h"

using namespace std;
using namespace cv;
using namespace PixelMapper;

class PixelMapperTest : public CPPUNIT_NS::TestFixture
{
  CPPUNIT_TEST_SUITE( PixelMapperTest );
  CPPUNIT_TEST( test_pixel_to_lonlat );
  CPPUNIT_TEST_SUITE_END();

protected:
  Point2f* test_pixel_array[4] = { new Point2f(0,0), new Point2f(0,0), new Point2f(0,0), new Point2f(0,0) };
  Point2f* test_lonlat_array[4] = { new Point2f(0,0), new Point2f(0,0), new Point2f(0,0), new Point2f(0,0) };
  Point2f* test_lonlat_origin = new Point2f(0,0);

  PixelMapperConfig* test_config = NULL;

public:
  void setUp() {
    test_config = new PixelMapperConfig(test_pixel_array, test_lonlat_array, test_lonlat_origin);
  };

protected:
  void test_pixel_to_lonlat(){
    vector<Point2f*> pixel_coordinates = {new Point2f(0, 0)};

    vector<Point2f*>* lonlat_coordinates = pixel_to_lonlat(*test_config, pixel_coordinates);
    cout << "lonlat_coordinates value" << (*lonlat_coordinates)[0]->x << endl;

    //How bout da memory cleanup??
  };
};
