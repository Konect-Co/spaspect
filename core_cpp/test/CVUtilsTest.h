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
using namespace CVUtils;

class CVUtilsTest : public CPPUNIT_NS::TestFixture
{
  CPPUNIT_TEST_SUITE( CVUtilsTest );
  CPPUNIT_TEST( test_compute_area );
  CPPUNIT_TEST( test_compute_intersection );
  CPPUNIT_TEST( test_compute_IoU );
  CPPUNIT_TEST( test_compute_IoA );
  CPPUNIT_TEST_SUITE_END();

protected:
  int boxA[4] = {50,50,100,100};
  int boxB[4] = {100,100,100,100};

public:
  void setUp() {
    cout << endl << "[INFO] Performing test setup" << endl;
  };

protected:
  void test_compute_area(){
    CPPUNIT_ASSERT_EQUAL(10000, compute_area(boxA));
    CPPUNIT_ASSERT_EQUAL(10000, compute_area(boxB));
  };
  void test_compute_intersection() {
    CPPUNIT_ASSERT_EQUAL(2500, compute_intersection(boxA, boxB));
  };
  void test_compute_IoU() {
    CPPUNIT_ASSERT_DOUBLES_EQUAL(0.14285714285714285, compute_IoU(boxA, boxB), 1e-5);
  };
  void test_compute_IoA() {
    CPPUNIT_ASSERT_DOUBLES_EQUAL(0.1, compute_IoA(boxA, boxB), 1e-5);
  };
};
