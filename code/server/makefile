TARGET: Serwer

CC=g++
FLAGS=-std=c++11 -lpthread -lsqlite3 -I.. -g
CFLAGS=-Wall -O2 $(FLAGS)
LFLAGS=-Wall $(FLAGS)
OBJS = main.o serwer.o client.o sha1.o

Serwer: $(OBJS)
	echo $(LFLAGS)
	$(CC) $(LFLAGS) $(OBJS) ../database/database.o -o bin/Serwer

serwer.o: serwer.cpp serwer.h
	$(CC) $(LFLAGS) serwer.cpp -c -o serwer.o

client.o: client.cpp client.h
	$(CC) $(LFLAGS) client.cpp -c -o client.o

main.o: main.cpp
	$(CC) $(LFLAGS) main.cpp -c -o main.o

sha1.o: sha1.cpp
	$(CC) $(LFLAGS) sha1.cpp -c -o sha1.o

.PHONY: clean TARGET
clean:
	rm -f $(target) *.o *~ *.bak
