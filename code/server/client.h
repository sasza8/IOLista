#ifndef _CLIENT_H_
#define _CLIENT_H_

#include "database/database.h"

#include <string>
using namespace std;

class Client
{
	int sock;
	
	ListDatabase::ListUser userDetails;
public:
	struct LoginDetails
	{
		string username;
		string password;
	};
	
	struct RegisterDetails
	{
		string username;
		string password;
		// inne - e-mail itp.
	};
	
	void setUserDetails(ListDatabase::ListUser dbUser);
	
	LoginDetails getLoginDetails();
	RegisterDetails getRegisterDetails();
	void loginOK();
	void loginFailed();
	void registerOK();
	void sendType(unsigned type);
	unsigned getType(); // odbiera od klienta sam typ pakietu
	
	Client(int sock);
	~Client();

};

#endif