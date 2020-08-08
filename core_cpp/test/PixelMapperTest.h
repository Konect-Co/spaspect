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
using namespace PixelMapper;

class PixelMapperTest : public CPPUNIT_NS::TestFixture
{
  CPPUNIT_TEST_SUITE( PixelMapperTest );
  CPPUNIT_TEST( test_pixel_to_lonlat );
  CPPUNIT_TEST_SUITE_END();

protected:
  int test_pixel_array[4][2] = { 0, 0, 0, 0, 0, 0, 0, 0 };
  int test_lonlat_array[4][2] = { 0, 0, 0, 0, 0, 0, 0, 0 };
  int test_lonlat_origin[2] = { 0, 0 };

  PixelMapperConfig *test_config = NULL;

public:
  void setUp() {
    test_config = PixelMapperConfig(*test_pixel_array, *test_lonlat_array, test_lonlat_origin);
  };

protected:
  void test_pixel_to_lonlat(){
    int pixel_coordinates[][2] = { 0, 0 };
    int lonlat_coordinates[][2] = pixel_to_lonlat(*test_config, *pixel_coordinates);
    cout << "lonlat_coordinates value" << lonlat_coordinates[0][0] << endl;
    CPPUNIT_ASSERT_DOUBLES_EQUAL( 1.0, 1.1, 0.05 );
    CPPUNIT_ASSERT( 1 == 0 );
    CPPUNIT_ASSERT( 1 == 1 );
  };
};
