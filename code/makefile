TARGET: serwer

CC	= cc
CFLAGS	= -Wall -O2
LFLAGS	= -Wall


echo-server: echo-server.o err.o
	$(CC) $(LFLAGS) $^ -o $@

echo-client: echo-client.o err.o
	$(CC) $(LFLAGS) $^ -o $@

.PHONY: clean TARGET
clean:
	rm -f $(target) *.o *~ *.bak
