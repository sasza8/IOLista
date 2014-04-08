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

void test_user(int sock, const char * username, const char * pass,
		const unsigned odpowiedz_serwera) {

	write(sock, CTS_LOGIN, sizeof(CTS_LOGIN));

	struct ctr_login_details temp;
	temp.username = username;
	temp.password = pass;

	write(sock, CTS_LOGIN_DETAILS, sizeof(CTS_LOGIN_DETAILS));
	write(sock, temp, sizeof(temp));

	const unsigned odpowiedz;
	read(sock, &odpowiedz, sizeof(odpowiedz));

	assert(odpowiedz==odpowiedz_serwera);
}

int main(int argc, char *argv[]){
	int sock;

	struct addrinfo addr_hints;
	struct addrinfo *addr_result;

	char buffer[BUFFER_SIZE];
	size_t len;
	ssize_t len2;

	if( argc != 3 )
		printf("URUCHAMIAC TAK: ./program adres_serwera port_serwera");

	if( debug )
		printf("<--------------------------------->\n address: %s\n port: %s\n",
				argv[1], argv[2]);

	// Laczymy sie po TCP z serwerem
	memset(&addr_hints, 0, sizeof(struct addrinfo));
	addr_hints.ai_family = AF_INET; // IPv4
	addr_hints.ai_socktype = SOCK_STREAM;
	addr_hints.ai_protocol = IPPROTO_TCP;
	if( getaddrinfo(argv[1], argv[2],
				&addr_hints, &addr_result) != 0 );

	// tworzymy socket zgodnie z informacjami z getaddrinfo
	sock = socket(addr_result->ai_family, addr_result->ai_socktype,
			addr_result->ai_protocol);
	if( sock < 0 );

	// laczymy sie z serwerem
	if( connect(sock, addr_result->ai_addr,
				addr_result->ai_addrlen) < 0);

	freeaddrinfo(addr_result);

	// JESTESMY POLACZENI Z SERWERM NA gniezdzie sock!
	// Czas sprawdzic jakies pierdoly
	// TODO

	// test1 - user: test || pass: testowa
	test_user(sock, "test", "testowa", STC_LOGINOK);
	//test2 - user: blad || pass: cokolwiek 
	test_user(sock, "blad", "cokolwiek666", STC_LOGINFAILED);

	return 0;
}



