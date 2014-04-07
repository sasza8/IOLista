TARGET: Serwer

CC=g++
CFLAGS=-Wall -O2 -std=c++11 -lpthread
LFLAGS=-Wall -std=c++11 -lpthread

Serwer: main.o serwer.o
	echo $(LFLAGS)
	$(CC) $(LFLAGS) main.o serwer.o -o bin/Serwer

serwer.o: serwer.cpp serwer.h
	$(CC) $(LFLAGS) serwer.cpp -c -o serwer.o

main.o: main.cpp
	$(CC) $(LFLAGS) main.cpp -c -o main.o

.PHONY: clean TARGET
clean:
	rm -f $(target) *.o *~ *.bak
