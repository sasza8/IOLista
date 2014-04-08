#ifndef _CLIENT_H_
#define _CLIENT_H_

#include <string>
using namespace std;

class Client
{
	int sock;
public:
	struct LoginDetails
	{
		string username;
		string password;
	};
	
	
	LoginDetails getLoginDetails();
	void loginOK();
	void loginFailed();
	void registerOK();
	void sendType(unsigned type);
	unsigned getType(); // odbiera od klienta sam typ pakietu
	
	Client(int sock);
	~Client();

};

#endif