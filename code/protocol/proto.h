#ifndef _PROTO_H_
#define _PROTO_H_


// typy pakietów przesyłane pomiędzy serwerem a klientem
// każdy pakiet musi się zaczynać typem
// CTS - pakiet przesylany od klienta do serwera
// STC - na odwrot

// --------------------- LOGOWANIE ----------------------
const unsigned CTS_LOGIN = 0x01; // sygnalizacja logowania, pusty pakiet
const unsigned CTS_LOGIN_DETAILS = 0x02; // nazwa uzytkownika i haslo
struct cts_login_details
{
	char username[200];
	char password[200];
};

const unsigned STC_LOGIN_OK = 0x03; // pusty
const unsigned STC_LOGIN_FAILED = 0x04; // pusty


// -------------------REJESTRACJA-----------------------
const unsigned CTS_REGISTER = 0x1001; // sygnalizacja rejestracji nowego uzytkownika, pusty pakiet
const unsigned CTS_REGISTER_DETAILS = 0x1002; // szczegoly rejestracji
struct cts_register_details
{
	char username[200];
	char password[200];
	// jakies inne pola - TODO
};

const unsigned STC_REGISTER_OK = 0x1003;

// ---------------------POBIERANIE ZADAN--------------------------
const unsigned CTS_GET_TASKS = 0x3001; // zadanie wyslania wszystkich zadan z danej listy
struct cts_get_tasks
{
	int id; // id parenta (wartosc ujemna oznacza null)
};

const unsigned STC_START_TASKS = 0x3002;
struct stc_start_tasks
{
	int number; // liczba taskow, ktore beda przeslane
};

const unsigned STC_TASK = 0x3003;
struct stc_task
{
	int id;
	char description[400]0;
	char owner[200];
	bool done;
	int createdon;
	int lastchange;
};

// -------------------DODAWANIE ZADAN----------------------------------
const unsigned CTS_ADD_TASK = 0x4001;
struct cts_add_task
{
	int parent;
	char description[4000];
};

#endif
