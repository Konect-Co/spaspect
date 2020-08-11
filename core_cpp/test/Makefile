CC=g++
CCFLAGS =
LIBS = -lopencv_core -lopencv_imgcodecs -lopencv_videoio

all: executable

debug: CCFLAGS += -DDEBUG -g
debug: executable

executable:
	$(CC) $(CCFLAGS) -c -o RunTests.o RunTests.cpp
	$(CC) $(CCFLAGS) -c -o Main.o Main.cpp
	libtool --mode=link $(CC) $(CCFLAGS) $(LIBS) -o a.out RunTests.o Main.o /usr/local/src/cppunit/libcppunit.la -ldl

clean:
	rm -rf *.o a.out
