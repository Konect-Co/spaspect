#include <cppunit/config/SourcePrefix.h>

//#include "ExampleTestCase.h"
#include "PixelMapperTest.h"

//CPPUNIT_TEST_SUITE_REGISTRATION( ExampleTestCase );
CPPUNIT_TEST_SUITE_REGISTRATION( PixelMapperTest );

/*
Methods:
CPPUNIT_ASSERT( bool cond )
CPPUNIT_ASSERT_EQUAL(int/long a, int/long b)
CPPUNIT_ASSERT_DOUBLES_EQUAL(double a, double b, double tolerance)
*/

// Another type of test -- can add directly to cpp file
/*
class FixtureTest : public CPPUNIT_NS::TestFixture
{
};

CPPUNIT_TEST_FIXTURE(FixtureTest, testEquals)
{
  CPPUNIT_ASSERT_EQUAL( 12, 12 );
}

CPPUNIT_TEST_FIXTURE(FixtureTest, testAdd)
{
  double result = 2.0 + 2.0;
  CPPUNIT_ASSERT( result == 4.0 );
}
*/