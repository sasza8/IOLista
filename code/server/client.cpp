#include "client.h"
#include "protocol/proto.h"
#include "database/database.h"

#include <unistd.h>
#include <sys/socket.h>
#include <string>
using namespace std;

Client::Client(int sock) : sock(sock) {}

Client::~Client()
{
	close(sock);
}

void Client::setUserDetails(ListDatabase::ListUser dbUser)
{
	userDetails = dbUser;
}

Client::LoginDetails Client::getLoginDetails()
{
	int type = getType();
	if(type != CTS_LOGIN_DETAILS);
		// wyjateczek
	cts_login_details details;
	recv(sock, &details, sizeof(details), 0);
	Client::LoginDetails ret;
	ret.username = details.username;
	ret.password = details.password;
	return ret;
}

Client::RegisterDetails Client::getRegisterDetails()
{
	int type = getType();
	if(type != CTS_REGISTER_DETAILS);
		// wyjateczek
	cts_register_details details;
	recv(sock, &details, sizeof(details), 0);
	Client::RegisterDetails ret;
	ret.username = details.username;
	ret.password = details.password;
	return ret;
}

void Client::sendType(unsigned type)
{
	send(sock, &type, sizeof(type), 0);
}

unsigned Client::getType()
{
	int type;
	recv(sock, &type, sizeof(type), 0);
	return type;
}

void Client::loginOK()
{
	sendType(STC_LOGIN_OK);
}

void Client::loginFailed()
{
	sendType(STC_LOGIN_FAILED);
}

void Client::registerOK()
{
	sendType(STC_REGISTER_OK);
}
