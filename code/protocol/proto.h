#ifndef _PROTO_H_
#define _PROTO_H_


// typy pakietów przesyłane pomiędzy serwerem a klientem
// każdy pakiet musi się zaczynać typem
// CTS - pakiet przesylany od klienta do serwera
// STC - na odwrot

const unsigned CTS_LOGIN = 0x01; // sygnalizacja logowania, pusty pakiet
const unsigned CTS_USERNAME = 0x02; // nazwa uzytkownika, string nullterminated
const unsigned STC_SALT = 0x03; // salt, string nullterminated
const unsigned CTS_PASSWORDHASH = 0x04; // hash hasla, string nullterminated

const unsigned CTS_REGISTER = 0x10; // sygnalizacja rejestracji nowego uzytkownika

#endif