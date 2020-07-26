CC=g++
CCFLAGS = 
LIBS = -lopencv_core -lopencv_imgcodecs -lopencv_videoio

all: executable

debug: CCFLAGS += -DDEBUG -g
debug: executable

executable:
	$(CC) $(CCFLAGS) core.cpp $(LIBS)

clean:
	rm a.out