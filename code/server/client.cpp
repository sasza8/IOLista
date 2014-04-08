#include "client.h"
#include "protocol/proto.h"
#include "database/database.h"

#include <unistd.h>
#include <sys/socket.h>
#include <string>
#include <cstring>
using namespace std;

Client::Client(int sock) : sock(sock) {}

Client::~Client()
{
	close(sock);
}

void Client::setUserDetails(ListDatabase::ListUser dbUser)
{
	userDetails = dbUser;
}

Client::LoginDetails Client::getLoginDetails()
{
	unsigned type = getType();
	if(type != CTS_LOGIN_DETAILS);
		// wyjateczek
	cts_login_details details;
	recv(sock, &details, sizeof(details), 0);
	Client::LoginDetails ret;
	ret.username = details.username;
	ret.password = details.password;
	return ret;
}

Client::RegisterDetails Client::getRegisterDetails()
{
	unsigned type = getType();
	if(type != CTS_REGISTER_DETAILS);
		// wyjateczek
	cts_register_details details;
	recv(sock, &details, sizeof(details), 0);
	Client::RegisterDetails ret;
	ret.username = details.username;
	ret.password = details.password;
	return ret;
}

Client::TaskDetails Client::getTaskDetails()
{
	cts_add_task details;
	recv(sock, &details, sizeof(details), 0);
	
	Client::TaskDetails ret;
	ret.description = details.description;
	ret.parent = details.parent < 0 ? -1 : details.parent;
	return ret;
}

int Client::getTasksParent()
{
	cts_get_tasks details;
	recv(sock, &details, sizeof(details), 0);
	return details.id;
}

void Client::sendType(unsigned type)
{
	send(sock, &type, sizeof(type), 0);
}

unsigned Client::getType()
{
	int type;
	recv(sock, &type, sizeof(type), 0);
	return type;
}

void Client::loginOK()
{
	sendType(STC_LOGIN_OK);
}

void Client::loginFailed()
{
	sendType(STC_LOGIN_FAILED);
}

void Client::registerOK()
{
	sendType(STC_REGISTER_OK);
}

void Client::startSendingTasks(int number)
{
	sendType(STC_START_TASKS);
	stc_start_tasks details;
	details.number = number;
	send(sock, &details, sizeof(details), 0);
}

void Client::sendTask(ListDatabase::ListTask task)
{
	sendType(STC_TASK);
	stc_task details;
	details.id = task.id;
	strncpy(details.description, task.description.c_str(), sizeof(details.description)-1);
	// TODO: przesylac dane o ownerze, trzeba je wyciagnac z bazy
	details.done = task.done;
	details.createdon = task.created_on;
	details.lastchange = task.last_change;
	
	send(sock, &details, sizeof(details), 0);
}

unsigned Client::getID()
{
	return userDetails.id;
}

string Client::getUsername()
{
	return userDetails.login;
}
