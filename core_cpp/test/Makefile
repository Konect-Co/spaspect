all:
	g++ -c -o RunTests.o RunTests.cpp
	g++ -c -o Main.o Main.cpp
	libtool --mode=link g++ -o a.out RunTests.o Main.o /usr/local/src/cppunit/libcppunit.la -ldl

clean:
	rm -rf *.o a.out
