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
}

const unsigned STC_LOGINOK = 0x03;
const unsigned STC_LOGINFAILED = 0x04;

const unsigned CTS_REGISTER = 0x1001; // sygnalizacja rejestracji nowego uzytkownika
const unsigned CTS_REGISTER_DETAILS = 0x1002; // szczegoly rejestracji
struct cts_register_details
{
	char username[200];
	char password[200];
	// jakies inne pola - TODO
}

const unsigned 

#endif