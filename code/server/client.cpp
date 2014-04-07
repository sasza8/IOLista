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

string Client::getUsername()
{
	char buffer[200];
	int len = recv(sock, buffer, sizeof(buffer)-1, 0);
	buffer[len] = '\0';
	return string(buffer);
}

string Client::getPasswordHash(string salt)
{
	send(sock, salt.c_str(), salt.length(), 0);
	unsigned type;
	recv(sock, &type, sizeof(type), 0);
	if(type != CTS_PASSWORDHASH);
		// rzucamy wyjątek!
	char buffer[200];
	int len = recv(sock, buffer, sizeof(buffer)-1, 0);
	buffer[len] = '\0';
	return string(buffer);
}

int Client::getType()
{
	return 0;
}
