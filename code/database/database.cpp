//#include <sqlite3.h>
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



void ListDatabase::ListUser::getID(sqlite3* db)
{
	id = new UserID_t();
	*id = sqlite3_last_insert_rowid(db); //!!! wywali sie przy wspolbieznosci
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
	getID(db);
}

ListDatabase::ListUser ListDatabase::addUser(Text_t login, Text_t pass, Text_t salt,
					Text_t f_name, Text_t l_name, Text_t email)
{
	open();
	ListUser tmp = ListUser(login, pass, salt, f_name, l_name, email);
	tmp.insert(db);
	close();
	return tmp;
}













void ListDatabase::ListTask::getID(sqlite3* db)
{
	id = new UserID_t();
	*id = sqlite3_last_insert_rowid(db); //!!! wywali sie przy wspolbieznosci
}



void ListDatabase::ListTask::insert(sqlite3* db)
{ //TODO injctions!!! 
	/*char *zErrMsg = 0;
	std::ostringstream oss;
	oss << "INSERT INTO Tasks (Description, Owner, ParentID, ChildCounter, Done, CreatedOn, LastChange) "
	"VALUES ('"<< description <<"'," << owner_id ? owner_id : "NULL" << ","
	<< parent_id ? parent_id : "NULL" << "," << child_ct << "," << done << "," << "CURRENT_TIMESTAMP,CURRENT_TIMESTAMP" <<");";
	if(sqlite3_exec(db, oss.str().c_str(), nothing, 0, &zErrMsg)!= SQLITE_OK )
	{
		fprintf(stderr, "SQL error: %s\n", zErrMsg);
		sqlite3_free(zErrMsg);
	}
	oss.clear();
	getID(db);*/
}






/*
int main()
{
	ListDatabase x = ListDatabase("hehe");
	x.addUser("pikaczu32", "aa", "aa", "aa", "aa", "aa");
} */



