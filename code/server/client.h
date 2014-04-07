#ifndef _CLIENT_H_
#define _CLIENT_H_

#include <string>
using namespace std;

class Client
{
	int sock;
public:
	string getUsername();
	string getPasswordHash();
	
	
	Client(int sock);
	~Client();
};

#endif