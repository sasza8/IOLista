#ifndef _SERVER_H_
#define _SERVER_H_

#include <string>
using namespace std;

#include "client.h"
#include "database/database.h"

class Server
{
	ListDatabase db;
	
	void serveClient(int sock);
	
	static string generateSalt();
public:	
	void Listen();
	bool loginClient(Client &client);
	bool registerClient(Client &client);
	
	Server();
	~Server();
};

#endif