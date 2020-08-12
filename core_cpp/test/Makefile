CC=g++
CCFLAGS=
LIBS=-lopencv_core -lopencv_imgcodecs -lopencv_videoio -lopencv_imgproc

all: executable

debug: CCFLAGS += -DDEBUG -g
debug: executable

executable:
	$(CC) $(CCFLAGS) -o a.out RunTests.cpp Main.cpp -lcppunit-1.15 -lcppunit -ldl -L/usr/local/lib -lopencv_core -lopencv_imgcodecs -lopencv_videoio -lopencv_imgproc

clean:
	rm -rf *.o a.out