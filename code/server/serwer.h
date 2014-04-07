#ifndef _SERVER_H_
#define _SERVER_H_

#include <string>
using namespace std;

#include "client.h"

class Server
{
	void serveClient(int sock);
	string getSaltOfUser(string username); // wyciaga z bazy salta danego usera
public:
	void Listen();
	bool loginClient(Client client);
};

#endif