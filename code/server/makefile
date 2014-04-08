TARGET: Serwer

CC=g++
FLAGS=-std=c++11 -lpthread -I..
CFLAGS=-Wall -O2 $(FLAGS)
LFLAGS=-Wall $(FLAGS)
OBJS = main.o serwer.o client.o

Serwer: $(OBJS)
	echo $(LFLAGS)
	$(CC) $(LFLAGS) $(OBJS) -o bin/Serwer

serwer.o: serwer.cpp serwer.h
	$(CC) $(LFLAGS) serwer.cpp -c -o serwer.o

client.o: client.cpp client.h
	$(CC) $(LFLAGS) client.cpp -c -o client.o

main.o: main.cpp
	$(CC) $(LFLAGS) main.cpp -c -o main.o

.PHONY: clean TARGET
clean:
	rm -f $(target) *.o *~ *.bak