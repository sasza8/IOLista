#include <sqlite3.h>
#include <cstdio>
#include <cstring>
#include <cstdlib>
#include <iostream>


#include <sstream>

using namespace std;



#include "database.h"

ListDatabase::ListDatabase(std::string filename)
{
	name = filename;
}

ListDatabase::~ListDatabase()
{
}

void ListDatabase::open()
{
	if(sqlite3_open(name.c_str(), &db))
		std::cout << "baza nie otwarta" << std::endl;//throw OpenDBException
}

void ListDatabase::close()
{
	sqlite3_close(db);
}


/*
UserID_t* id;
		Text_t login;
		Text_t pass;
		Text_t salt;
		Text_t f_name;
		Text_t l_name;
		Text_t email;*/

UserID_t tmp_id; // TODO jakis mutex? jak to zrobic lepiej??
int ListDatabase::ListUser::idSelect(void *NotUsed, int argc, char **argv, char **azColName)
{
	for(int i=0; i<argc; i++){
      printf("%s = %s\n", azColName[i], argv[i] ? argv[i] : "NULL");
   }
   tmp_id = atoi(argv[0]);
   return 0;
}

void ListDatabase::ListUser::getID()
{
	std::ostringstream oss2;
	oss2 << "SELECT UserID FROM Users WHERE Login = '" << login <<  "';";
	if(sqlite3_exec(db, oss2.str().c_str(), idSelect, 0, &zErrMsg)!= SQLITE_OK )
	{
		// throw coś
		return;
	}
	id = new UserID_t();
	*id = tmp_id;
	std::cout << "moje id " << *id << std::endl; 
}

void ListDatabase::ListUser::insert(sqlite3* db)
{ //TODO injctions!!! 
	char *zErrMsg = 0;
	std::ostringstream oss;
	oss << "INSERT INTO Users (Login, Password, Salt, FirstName, LastName, Email) "
	"VALUES ('"<< login <<"','" << pass << "','" << salt << "','" << f_name << "','" << l_name << "','" << email <<"');";
	if(sqlite3_exec(db, oss.str().c_str(), nothing, 0, &zErrMsg)!= SQLITE_OK )
	{
		fprintf(stderr, "SQL error: %s\n", zErrMsg);
		sqlite3_free(zErrMsg);
	}
	oss.clear();
	getID();
}

ListDatabase::ListUser ListDatabase::addUser(Text_t login, Text_t pass, Text_t salt,
					Text_t f_name, Text_t l_name, Text_t email)
{
	open();
	ListUser tmp = ListUser(login, pass, salt, f_name, l_name, email).insert(db);
	close();
	return tmp;
}

int main()
{
	ListDatabase x = ListDatabase("hehe");
	x.addUser("pikacz32", "aa", "aa", "aa", "aa", "aa");
}



