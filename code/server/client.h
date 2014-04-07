#ifndef _CLIENT_H_
#define _CLIENT_H_

#include <string>
using namespace std;

class Client
{
	int sock;
public:
	string getUsername();
	string getPasswordHash(string salt); // przesyla klientowi salta i odbiera od niego hash
	int getType(); // odbiera od klienta sam typ pakietu
	
	
	Client(int sock);
	~Client();
};

#endif