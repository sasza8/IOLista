#include <sys/types.h>
#include <sys/socket.h>
#include <netinet/in.h>

#include <iostream>
#include <thread>
#include <cstdio>
#include <cstring>
#include <unistd.h>
using namespace std;

#include "serwer.h"
#include "protocol/proto.h"

string Server::generateSalt()
{
	FILE *random = fopen("/dev/urandom", "rb");
	string salt;
	for(int i = 0; i < 20; i++)
	{
		unsigned char c;
		fread(&c, sizeof(c), 1, random);
		c %= 95; // mamy 95 drukowalnych znakow ascii
		c += 0x20; // pierwszy na pozycji 0x20
		salt += c;
	}
	return salt;
}

void Server::serveClient(int sock)
{
	Client client(sock);
	int type = client.getType();
	switch(type)
	{
		case CTS_LOGIN:
			if(loginClient(client) == false)
				return;
			break;
		case CTS_REGISTER:
			registerClient(client);
			return;
			break;
		default:
			// wysylamy info o bledzie
			return;
	}
}

bool Server::loginClient(Client client)
{
	Client::LoginDetails loginDetails = client.getLoginDetails();
	// szukamy usera w bazie
	printf("Proba zalogowania uzytkownika %s:%s\n", loginDetails.username.c_str(), loginDetails.password.c_str());
	if(loginDetails.username == "test" && loginDetails.password == "testowa")
	{
		printf("Sukces\n");
		client.loginOK();
		return true;
	}
	else
	{
		printf("Porazka\n");
		client.loginFailed();
		return false;
	}
}

bool Server::registerClient(Client client)
{
	Client::RegisterDetails registerDetails = client.getRegisterDetails();
	// dopisujemy sobie usera w bazie, sprawdzamy czy konfliktuje itp. itp.
	client.registerOK();
}

void Server::Listen()
{
	const int PORT_NUM = 16661; // pracujemy na fajnym porcie kse

	struct sockaddr_in server_address;
	struct sockaddr_in client_address;

	// otwieramy gniazdo
	int serverSock = socket(PF_INET, SOCK_STREAM, 0); // creating IPv4 TCP socket
	int yes = 1;
	if (setsockopt(serverSock, SOL_SOCKET, SO_REUSEADDR, &yes, sizeof(int)) < 0);
	if (serverSock < 0);
	// after socket() call; we should close(sock) on any execution path;
	// since all execution paths exit immediately, sock would be closed when program terminates

	server_address.sin_family = AF_INET; // IPv4
	server_address.sin_addr.s_addr = htonl(INADDR_ANY); // listening on all interfaces
	server_address.sin_port = htons(PORT_NUM); // listening on port PORT_NUM

	// laczymy socket z portem i addressem naszym
	if (bind(serverSock, (struct sockaddr *) &server_address, sizeof(server_address)) < 0);

	// nasluchujemy! chujemy!
	if (listen(serverSock, 0) < 0);

	while(true)
	{
		socklen_t client_address_len = sizeof(client_address);
		// pobieramy polaczenie z sock! na nowym msg_sock to trzymamy
		int clientSock = accept(serverSock, (struct sockaddr *) &client_address, &client_address_len);
		
		if (clientSock < 0);
		
		thread( [&]()->void{ this->serveClient(clientSock); } ).detach();
	}
	

}


