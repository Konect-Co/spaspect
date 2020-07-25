CC=g++
CCFLAGS = 

all: executable

debug: CCFLAGS += -DDEBUG -g
debug: executable

executable:
	$(CC) $(CCFLAGS) core.cpp

clean:
	rm a.out