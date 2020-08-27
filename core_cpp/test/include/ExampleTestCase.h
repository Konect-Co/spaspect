#include <cppunit/extensions/HelperMacros.h>

class ExampleTestCase : public CPPUNIT_NS::TestFixture
{
  CPPUNIT_TEST_SUITE( ExampleTestCase );
  CPPUNIT_TEST( test1 );
  CPPUNIT_TEST( test2 );
  CPPUNIT_TEST( test3 );
  CPPUNIT_TEST( test4 );
  CPPUNIT_TEST_SUITE_END();

protected:
  double m_value1;
  double m_value2;

public:
void setUp() {
  m_value1 = 2.0;
  m_value2 = 3.0;
};

protected:
  void test1(){
    CPPUNIT_ASSERT_DOUBLES_EQUAL( 1.0, 1.1, 0.05 );
    CPPUNIT_ASSERT( 1 == 0 );
    CPPUNIT_ASSERT( 1 == 1 );
  };
  void test2(){
    CPPUNIT_ASSERT (1 == 2);
  };
  void test3(){
    double result = m_value1 + m_value2;
    CPPUNIT_ASSERT( result == 6.0 );
  };
  void test4(){
    long* l1 = new long(12);
    long* l2 = new long(12);

    CPPUNIT_ASSERT_EQUAL( 12, 12 );
    CPPUNIT_ASSERT_EQUAL( 12L, 12L );
    CPPUNIT_ASSERT_EQUAL( *l1, *l2 );

    delete l1;
    delete l2;

    CPPUNIT_ASSERT( 12L == 12L );
    CPPUNIT_ASSERT_EQUAL( 12, 13 );
    CPPUNIT_ASSERT_DOUBLES_EQUAL( 12.0, 11.99, 0.5 );
  };
};
