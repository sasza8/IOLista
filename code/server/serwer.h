#ifndef _SERVER_H_
#define _SERVER_H_

#include "client.h"

class Server
{
	void serveClient(int sock);
	string getSaltOfUser()
public:
	void Listen();
	bool loginClient(Client client);
};

#endif