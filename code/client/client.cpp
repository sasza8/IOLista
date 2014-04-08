#include <sys/types.h>
#include <sys/socket.h>
#include <netdb.h>
#include <stdio.h>
#include <string.h>
#include <unistd.h>
#include <stdlib.h>
#include <netinet/in.h>
#include <arpa/inet.h>

#include "protocol/proto.h"
#include <assert.h>

#define MAX_STRING 100
#define BUFFER_SIZE 10001

#define debug 1

char *ip, *port;

void test_user(int sock, const char * username, const char * pass,
		const unsigned odpowiedz_serwera) {

	int tempsnd = CTS_LOGIN;
	send(sock, &tempsnd, sizeof(tempsnd), 0);

	struct cts_login_details temp;
	strncpy(temp.username, username, sizeof(temp.username)-1);
	strncpy(temp.password, pass, sizeof(temp.password)-1);

	tempsnd = CTS_LOGIN_DETAILS;
	send(sock, &tempsnd, sizeof(tempsnd), 0);
	send(sock, &temp, sizeof(temp), 0);

	unsigned odpowiedz;
	recv(sock, &odpowiedz, sizeof(odpowiedz), 0);
	printf("%u\n", odpowiedz);

	assert(odpowiedz==odpowiedz_serwera);
}

int conn()
{
	int sock;

	struct addrinfo addr_hints;
	struct addrinfo *addr_result;

	char buffer[BUFFER_SIZE];
	size_t len;
	ssize_t len2;

	if( debug )
		printf("<--------------------------------->\n address: %s\n port: %s\n",
				ip, port);

	// Laczymy sie po TCP z serwerem
	memset(&addr_hints, 0, sizeof(struct addrinfo));
	addr_hints.ai_family = AF_INET; // IPv4
	addr_hints.ai_socktype = SOCK_STREAM;
	addr_hints.ai_protocol = IPPROTO_TCP;
	if( getaddrinfo(ip, port,
				&addr_hints, &addr_result) != 0 );

	// tworzymy socket zgodnie z informacjami z getaddrinfo
	sock = socket(addr_result->ai_family, addr_result->ai_socktype,
			addr_result->ai_protocol);
	if( sock < 0 );

	// laczymy sie z serwerem
	if( connect(sock, addr_result->ai_addr,
				addr_result->ai_addrlen) < 0);

	freeaddrinfo(addr_result);
	
	return sock;
}

int main(int argc, char *argv[]){
	
	if( argc != 3 )
		printf("URUCHAMIAC TAK: ./program adres_serwera port_serwera");
	
	ip = argv[1];
	port = argv[2];

	// JESTESMY POLACZENI Z SERWERM NA gniezdzie sock!
	// Czas sprawdzic jakies pierdoly
	// TODO

	// test1 - user: test || pass: testowa
	int sock = conn();
	test_user(sock, "test", "testowa", STC_LOGIN_OK);
	//test2 - user: blad || pass: cokolwiek 
	sock = conn();
	test_user(sock, "blad", "cokolwiek666", STC_LOGIN_FAILED);

	return 0;
}



