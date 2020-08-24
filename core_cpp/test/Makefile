CC=g++
CCFLAGS=
LIBS=-L/usr/local/lib -lcppunit -ldl -lopencv_core -lopencv_imgcodecs -lopencv_videoio -lopencv_imgproc
FILES=../src/CVUtils.cpp ../src/Track.cpp ../src/DashboardInfo.cpp ../src/PixelMapper.cpp ../src/CVOutput.cpp

all: executable

debug: CCFLAGS += -DDEBUG -g
debug: executable

executable:
	$(CC) $(CCFLAGS) -I ../include -o a.out RunTests.cpp Main.cpp $(FILES) $(LIBS)

clean:
	rm -rf *.o a.out
