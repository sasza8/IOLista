#ifndef _PROTO_H_
#define _PROTO_H_


// typy pakietów przesyłane pomiędzy serwerem a klientem
// każdy pakiet musi się zaczynać typem
// CTS - pakiet przesylany od klienta do serwera
// STC - na odwrot

const unsigned CTS_LOGIN = 0x01; // sygnalizacja logowania, pusty pakiet
const unsigned CTS_LOGIN_DETAILS = 0x02; // nazwa uzytkownika i haslo
struct cts_login_details
{
	char username[200];
	char password[200];
};

const unsigned STC_LOGIN_OK = 0x03; // pusty
const unsigned STC_LOGIN_FAILED = 0x04; // pusty

const unsigned CTS_REGISTER = 0x1001; // sygnalizacja rejestracji nowego uzytkownika, pusty pakiet
const unsigned CTS_REGISTER_DETAILS = 0x1002; // szczegoly rejestracji
struct cts_register_details
{
	char username[200];
	char password[200];
	// jakies inne pola - TODO
};

const unsigned STC_REGISTER_OK = 0x1003;

const unsigned CTS_GET_LISTS = 0x2001; // zadanie wyslania wszystkich list, do ktorych user ma dostep, pusty pakiet
const unsigned STC_LISTS_BEGIN = 0x2002; // naglowek listy list
struct stc_list_begin
{
	int number; // liczba list, ktore beda przeslane
};

const unsigned STC_LIST = 0x2003;
struct stc_list
{
	int id;
	char name[200];
};

const unsigned CTS_GET_TASKS = 0x2004; // zadanie wyslania wszystkich zadan z danego pakietu


#endif