#include <sys/types.h>
#include <sys/socket.h>
#include <netdb.h>
#include <unistd.h>

#include <cstdlib>
#include <cstdio>
#include <cstring>

#include "../protocol/proto.h"
#include <assert.h>

#define debug 1

char *ip, *port;
char user[100];
char pass[100];

void zaloguj(int sock, const char *username, const char *pass){
	int tempsnd = CTS_LOGIN;
	send(sock, &tempsnd, sizeof(tempsnd), 0);

	struct cts_login_details temp;
	strncpy(temp.username, username, sizeof(temp.username)-1);
	strncpy(temp.password, pass, sizeof(temp.password)-1);

	tempsnd = CTS_LOGIN_DETAILS;
	send(sock, &tempsnd, sizeof(tempsnd), 0);
	send(sock, &temp, sizeof(temp), 0);
}



void test_user(const int sock, const char *username, const char *pass,
		const unsigned odpowiedz_serwera) {

	zaloguj(sock, username, pass);

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

void wyswietl_listy(const int conn) {
	// Wysylamy zadanie 
	int tempsnd = CTS_GET_LISTS;
	send(sock, &tempsnd, sizeof(tempsnd), 0);

	int tempresp;
	do{ // czekamy na pakiet CTS_LISTS_BEGIN
		recv(sock, &tempresp, sizeof(tempresp), 0);
	} while tempresp != CTS_LISTS_BEGIN;
	int lists_number;
	recv(sock, &lists_number, sizeof(lists_number), 0);

	for( int i = 0 ; i < lists_number ; i++ ){
		do{ // czekamy na pakiet STC_LIST
			recv(sock, &tempresp, sizeof(tempresp), 0);
		} while tempresp != STC_LIST;
		struct stc_list list;
		// TODO - tutaj moze inicjalizacja? 
		// id na 0, name na FAIL albo cos takiego
		recv(sock, &list, sizeof(list), 0);
		printf("ID: %d, ZADANIE: %s\n", list.id, list.name);
	}
}

void test_zaloguj() {
	printf("Prosze sie zalogowac, jezeli program zapyta o uzytkowniak i haslo powtornie ---> nie udalpo sie zalogowac");
	do{
		printf("Prosze podac uzytkownika: ");
		scanf("%s\n", user);
		printf("Prosze podac haslo: ");
		scanf("%s\n", pass);
		zaloguj(conn, user, pass);

		unsigned odpowiedz;
		recv(sock, &odpowiedz, sizeof(odpowiedz), 0);

	} while odpowiedz != STC_LOGIN_OK;
}

void test_komunikat_zalogowany(){
	printf("Jestes zalogowany jako uzytkownik %s\n", user);
	printf("Wpisz:\n");
	printf("	1 - aby zobaczyc swoje zadania\n");
	printf("	2 - aby dodac nowe zadanie\n");
	printf("	ctrl^c aby wyjsc z programu ;)\n");
}

void test_komendy() {
	test_komunikat_zalogowany();
	while( 1 ) {
		int komenda;
		scanf("%d", &komenda);
		switch komenda {
			case 1:
				printf("Zadania uzytkownika %s:\n", user);
				wyswietl_listy(sock);
				break;
			case 2:
				//TODO

				break;
			default:
				printf("Zla komenda\n");
		}
	}
}

int main(int argc, char *argv[]){
	
	if( argc != 3 )
		printf("URUCHAMIAC TAK: ./program adres_serwera port_serwera");
	
	ip = argv[1];
	port = argv[2];

//	// test1 - user: test || pass: testowa
//	int sock = conn();
//	test_user(sock, "test", "testowa", STC_LOGIN_OK);
//	//test2 - user: blad || pass: cokolwiek 
//	sock = conn();
//	test_user(sock, "blad", "cokolwiek666", STC_LOGIN_FAILED);

	sock = conn();



