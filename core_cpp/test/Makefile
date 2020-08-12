CC=g++
CCFLAGS=
LIBS=-L/usr/local/lib -lcppunit -ldl -lopencv_core -lopencv_imgcodecs -lopencv_videoio -lopencv_imgproc

all: executable

debug: CCFLAGS += -DDEBUG -g
debug: executable

executable:
	$(CC) $(CCFLAGS) -o a.out RunTests.cpp Main.cpp $(LIBS)

clean:
	rm -rf *.o a.out
