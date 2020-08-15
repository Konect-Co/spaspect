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

/*
from core import PixelMapper

pixel_coords = [[330,250],[50,370],[945,395],[815,245]]
lonlat_coords = [[-73.984976, 40.759271],[-73.985132, 40.759316], [-73.985201, 40.759196],[-73.985035,40.759104]]

pm = PixelMapper.PixelMapper(pixel_coords, lonlat_coords, lonlat_coords[0])

"""
Value of pm.M
array([[-3.19845962e-03,  4.84332889e-01, -7.39855146e+01],
       [ 1.76231853e-03, -2.66824125e-01,  4.07592201e+01],
       [ 4.32324145e-05, -6.54634065e-03,  1.00000000e+00]])

Value of pm.invM
array([[ 3.05664837e+00, -1.25006380e+01,  7.35664052e+02],
       [ 1.56430248e+00, -8.87476957e-01,  1.51908645e+02],
       [ 1.05046712e-02, -5.46645604e-03,  1.00000000e+00]])

Value of pm.lat_const
111320

Value of pm.lon_const
30711.85548348597

Value of pm.lonlat_origin
[-73.984976, 40.759271]
"""

lonlat = pm.pixel_to_lonlat([100,200]) # ==> [-73.98457242314669, 40.75940737741828]
pixel = pm.lonlat_to_pixel([-73.985, 40.7592]) # ==> [543.7754262271288, 248.17036212679892]
_3D = pm.lonlat_to_3D([-73.985, 40.7592]) # ==> [-7.90371999981943, -0.7370845314884706, 0]
lonlat2 = pm._3D_to_lonlat([10,10,0]) # ==> [-73.98465039284137, 40.7593608311175]
*/

class PixelMapperTest : public CPPUNIT_NS::TestFixture
{
  CPPUNIT_TEST_SUITE( PixelMapperTest );
  CPPUNIT_TEST( test_pixel_to_lonlat );
  CPPUNIT_TEST( test_lonlat_to_pixel );
  CPPUNIT_TEST( test_lonlat_to_3D );
  CPPUNIT_TEST( test_3D_to_lonlat );
  CPPUNIT_TEST_SUITE_END();

protected:
  Point2f test_pixel_array[4] = { Point2f(330.,250.), Point2f(50.,370.), Point2f(945.,395.), Point2f(815.,245.) };
  Point2f test_lonlat_array[4] = { Point2f(-73.984976, 40.759271), Point2f(-73.985132, 40.759316), 
    Point2f(-73.985201, 40.759196), Point2f(-73.985035,40.759104) };
  Point2f* test_lonlat_origin = new Point2f(-73.984976, 40.759271);

  PixelMapperConfig* test_config = NULL;

public:
  void setUp() {
    cout << endl << "[INFO] Performing test setup" << endl;
    test_config = new PixelMapperConfig(test_pixel_array, test_lonlat_array, test_lonlat_origin);
  };

protected:
  void test_pixel_to_lonlat(){
    vector<Point2f*> pixel_coordinates = {new Point2f(100, 200)};
    vector<Point2f*>* lonlat_coordinates = pixel_to_lonlat(*test_config, pixel_coordinates);

    CPPUNIT_ASSERT_DOUBLES_EQUAL(-73.98457242314669, (*lonlat_coordinates)[0]->x, 1e-5 );
    CPPUNIT_ASSERT_DOUBLES_EQUAL(40.75940737741828, (*lonlat_coordinates)[0]->y, 1e-5 );

    cout << "[INFO] Performing memory cleanup" << endl;
    for (auto pixel_coord : pixel_coordinates)
      delete pixel_coord;
    for (auto lonlat_coord : *lonlat_coordinates)
      delete lonlat_coord;
    delete lonlat_coordinates;
  };
  void test_lonlat_to_pixel() {
    vector<Point2f*> lonlat_coordinates = {new Point2f(-73.985, 40.7592)};
    vector<Point2f*>* pixel_coordinates = lonlat_to_pixel(*test_config, lonlat_coordinates);

    CPPUNIT_ASSERT_DOUBLES_EQUAL(543.7754262271288, (*pixel_coordinates)[0]->x, 3 );
    CPPUNIT_ASSERT_DOUBLES_EQUAL(248.17036212679892, (*pixel_coordinates)[0]->y, 3 );

    cout << "[INFO] Performing memory cleanup" << endl;
    for (auto lonlat_coord : lonlat_coordinates)
      delete lonlat_coord;
    for (auto pixel_coord : *pixel_coordinates)
      delete pixel_coord;
    delete pixel_coordinates;
  };
  void test_lonlat_to_3D() {
    vector<Point2f*> lonlat_coordinates = {new Point2f(-73.985, 40.7592)};
    vector<Point3f*>* _3D_coordinates = lonlat_to_3D(*test_config, lonlat_coordinates);

    CPPUNIT_ASSERT_DOUBLES_EQUAL(-7.90371999981943, (*_3D_coordinates)[0]->x, .5 );
    CPPUNIT_ASSERT_DOUBLES_EQUAL(-0.7370845314884706, (*_3D_coordinates)[0]->y, .5 );
    CPPUNIT_ASSERT_DOUBLES_EQUAL(0, (*_3D_coordinates)[0]->z, 1e-2 );

    cout << "[INFO] Performing memory cleanup" << endl;
    for (auto lonlat_coord : lonlat_coordinates)
      delete lonlat_coord;
    for (auto _3D_coordinate : *_3D_coordinates)
      delete _3D_coordinate;
    delete _3D_coordinates;
  };
  void test_3D_to_lonlat() {
    vector<Point3f*> _3D_coordinates = {new Point3f(10,10,0)};
    vector<Point2f*>* lonlat_coordinates = _3D_to_lonlat(*test_config, _3D_coordinates);

    CPPUNIT_ASSERT_DOUBLES_EQUAL(-73.98465039284137, (*lonlat_coordinates)[0]->x, 1e-2 );
    CPPUNIT_ASSERT_DOUBLES_EQUAL(40.7593608311175, (*lonlat_coordinates)[0]->y, 1e-2 );

    cout << "[INFO] Performing memory cleanup" << endl;
    for (auto _3D_coordinate : _3D_coordinates)
      delete _3D_coordinate;
    for (auto lonlat_coordinate : *lonlat_coordinates)
      delete lonlat_coordinate;
    delete lonlat_coordinates;
  };
};
