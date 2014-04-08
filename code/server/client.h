#ifndef _CLIENT_H_
#define _CLIENT_H_

#include <string>
using namespace std;

class Client
{
	int sock;
public:
	cts_login_details getLoginDetails();
	void loginOK();
	void registerOK();
	void sendType(unsigned type);
	int getType(); // odbiera od klienta sam typ pakietu
	
	Client(int sock);
	~Client();
};

#endif