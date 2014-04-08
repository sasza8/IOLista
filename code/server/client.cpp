#include "client.h"
#include "protocol/proto.h"

#include <unistd.h>
#include <sys/socket.h>
#include <string>
using namespace std;

Client::Client(int sock) : sock(sock) {}

Client::~Client()
{
	close(sock);
}

cts_login_details Client::getLoginDetails()
{
	cts_login_details details;
	recv(sock, &details, sizeof(details), 0);
	return details;
}

void Client::loginOK()
{
	sendType(STC_LOGIN_OK);
}

void Client::registerOK()
{
	sendType(STC_REGISTER_OK);
}

void Client::sendType(unsigned type)
{
	send(sock, &type, sizeof(type), 0);
}

int Client::getType()
{
	return 0;
}
