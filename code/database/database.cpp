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

static int nothing(void *NotUsed, int argc, char **argv, char **azColName)
{
	return 0;
};
void ListDatabase::ListUser::insert(sqlite3* db)
{ //TODO injctions!!! 
	char *zErrMsg = 0;
	std::ostringstream oss;
	oss << "INSERT INTO Users (Login, Password, Salt, FirstName, LastName, Email) "
	"VALUES ('"<< login <<"','" << pass << "','" << salt << "','" << f_name << "','" << l_name << "','" << email <<"');";
	std::cout << oss.str() << std::endl;
	if(sqlite3_exec(db, oss.str().c_str(), nothing, 0, &zErrMsg)!= SQLITE_OK )
	{
		fprintf(stderr, "SQL error: %s\n", zErrMsg);
		sqlite3_free(zErrMsg);
	}
	
}

void ListDatabase::addUser(Text_t login, Text_t pass, Text_t salt,
					Text_t f_name, Text_t l_name, Text_t email)
{
	open();
	ListUser(login, pass, salt, f_name, l_name, email).insert(db);
	close();
}



