#include <sys/types.h>
#include <sys/socket.h>
#include <netdb.h>
#include <unistd.h>

#include <cstdlib>
#include <cstdio>
#include <cstring>

#include "../protocol/proto.h"
#include <assert.h>

char *ip, *port;
char user[100];
char pass[100];

// probuje sie zalogowac
// NIE SPRAWDZA odpowiedzi serwera!! czy FAIL czy OK trzeba sprawdzic samemu
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

// Laczy sie na podany z lini polecen adres i port, zwraca gniazdo polaczenia
int conn() {
	int sock;

	struct addrinfo addr_hints;
	struct addrinfo *addr_result;

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

// --------------------- KOMUNIKATY TEKSTOWE ----------------------
void test_komunikat_zalogowany(){
	printf("Jestes zalogowany jako uzytkownik %s\n", user);
	printf("Wpisz:\n");
	printf("	1 - aby zobaczyc swoje zadania\n");
	printf("	2 - aby dodac nowe zadanie\n");
	printf("	ctrl^c aby wyjsc z programu ;)\n");
}

void test_komunikat_dodaj_zadanie(){
	printf("Aby dodac nowe zadanie trzeba podac 2 wartosci:\n"
			"	ojciec - id ZADANIA, tworzone zadanie stanie sie "
			"podzadaniem zadania z id ojciec ( wpisac -1 "
			"gdy chcemy zeby zadanie nie bylo podzadaniem)\n"
			"	opis - tekstowy opis zadania\n"
	);
}

void test_komunikat_pobierz_zadania(){
	printf("Aby pobrac zadania trzeba wpisac id.\n"
			"ID oznacza ID zadania ktore chcemy pobrac\n"
			"Jezeli chcesz zobaczyc wszystkie zadania wpisz -1\n"
	);
}

// ---------------- FUNKCJE OBSLUGUJACE KOMUNIKATY ------------------
// odbiera i wyswietla 'number' zadan
// POMOCNICZA! uzywana przez funkcje wyswietl_zadania( ... )
void wyswietl_pomocnicza(const int sock, int number) {
	unsigned int temp;
	// wyswietlamy zadania
	for( int i = 0 ; i < number ; i++ ){
		printf("Probuje pobrac STC_TASK\n");
		recv(sock, &temp, sizeof(temp), 0);
		if (temp != STC_TASK) { printf("%x\n", temp); assert(false); }
		struct stc_task task;
		// TODO - tutaj moze inicjalizacja? 
		// id na 0, name na FAIL albo cos takiego
		printf("ID: %d\n"
				"DESCRIPTION: %s\n"
				"OWNER: N/A\n"
				"DONE: %s\n"
				"CREATEDON: %d\n"
				"LASTCHANGE: %d\n",
				task.id,
				task.description,
				//task.owner,
				task.done ? "true" : "false",
				task.createdon,
				task.lastchange
		);
		printf("========================================\n");
	}
}

// pobiera ID zadania, wyswietla wszystkie podzadania?
void wyswietl_zadania(const int sock) {
	test_komunikat_pobierz_zadania();

	int id;
	printf("prosze podac id: ");
	scanf("%d", &id);

	// Wysylamy pakiet i id zadania
	unsigned int temp = CTS_GET_TASKS;
	send(sock, &temp, sizeof(temp), 0); // CTS_GET_TASKS
	struct cts_get_tasks task_id;
	task_id.id = id;
	send(sock, &task_id, sizeof(task_id), 0);

	// czekamy na odpowiedni pakiet i odbieramy ilosc zadan
	printf("Probuje pobrac STC_START_TASKS...\n");
	recv(sock, &temp, sizeof(temp), 0);
	if (temp != STC_START_TASKS) assert(false);
	struct stc_start_tasks task_number;
	recv(sock, &task_number, sizeof(task_number), 0);

	// wyswietlamy zadania!
	printf("%d zadan\n", task_number.number);
	wyswietl_pomocnicza(sock, task_number.number);
}

// Pobiera z wejscia dane i wysyla je do serwera z odpowiednim pakietem
void dodaj_zadanie(const int sock) {
	test_komunikat_dodaj_zadanie();
	int parent_;
	char description_[4000];
	//TODO
	printf("prosze podad id: \n");
	scanf("%d", &parent_);
	printf("prosze podac opis: \n");
	scanf("%s", description_);

	struct cts_add_task msg;
	msg.parent = parent_;
	strncpy(msg.description, description_, sizeof(msg.description)-1);

	int tempsnd = CTS_ADD_TASK;
	send(sock, &tempsnd, sizeof(tempsnd), 0);
	send(sock, &msg, sizeof(msg), 0);
}

// ------------------ FUNKCJE TESTOWE --------------------------------
// pozwala testowac baze danych, wczytuje i reaguje na komendy
void test_komendy(const int sock) {
	test_komunikat_zalogowany();
	while( 1 ) {
		printf("Czekam na komende:  ");
		int komenda;
		scanf("%d", &komenda);
		switch( komenda ) {
			case 1:
				printf("Zadania uzytkownika %s:\n", user);
				wyswietl_zadania(sock);
				break;
			case 2:
				dodaj_zadanie(sock);
				break;
			default:
				printf("Zla komenda\n");
		}
	}
}

// probuje sie zalogowac do skutku! pobiera USER i PASS z stdin
void test_zaloguj(const int sock) {
	printf("Prosze sie zalogowac, jezeli program zapyta o uzytkowniak i haslo"
		   "	powtornie ---> nie udalo sie zalogowac\n");
	unsigned odpowiedz;
	do{
		printf("Prosze podac uzytkownika: \n");
		scanf("%s", user);
		printf("Prosze podac haslo:\n ");
		scanf("%s", pass);
		zaloguj(sock, user, pass);

		recv(sock, &odpowiedz, sizeof(odpowiedz), 0);

	} while (odpowiedz != STC_LOGIN_OK);
}
int main(int argc, char *argv[]){
	
	if( argc != 3 )
		printf("URUCHAMIAC TAK: ./program adres_serwera port_serwera\n");
	
	ip = argv[1];
	port = argv[2];
//	// test1 - user: test || pass: testowa
//	int sock = conn();
//	test_user(sock, "test", "testowa", STC_LOGIN_OK);
//	//test2 - user: blad || pass: cokolwiek 
//	sock = conn();
//	test_user(sock, "blad", "cokolwiek666", STC_LOGIN_FAILED);
	printf("Nawiazuje polaczenie...\n");
	int sock = conn();
	printf("Polaczenie nawiazane\n");
	test_zaloguj(sock);
	test_komendy(sock);
}



