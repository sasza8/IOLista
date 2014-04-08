
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
	char *zErrMsg = 0;
	std::ostringstream oss;
	oss << "INSERT INTO Tasks (Description, Owner, ParentID, ChildCounter, Done, CreatedOn, LastChange) VALUES ('"
	<< description <<"',";
	oss << owner_id;
	oss << ",";
	if(parent_id != nullptr)
		oss << *parent_id;
	else
		oss << "NULL";
	oss << "," << child_ct << "," << done << "," << "CURRENT_TIMESTAMP,CURRENT_TIMESTAMP" <<");";
	
	//std::cout << oss.str() << std::endl;
	
	
	if(sqlite3_exec(db, oss.str().c_str(), nothing, 0, &zErrMsg)!= SQLITE_OK )
	{
		fprintf(stderr, "SQL error: %s\n", zErrMsg);
		sqlite3_free(zErrMsg);
	}
	//oss.clear();
	getID(db);
}

ListDatabase::ListTask ListDatabase::addTask(Text_t description, UserID_t owner_id, 
					TaskID_t* parent_id, TaskDone_t done)
{
	open();
	ListTask task = ListTask(description, owner_id, parent_id, done);
	task.insert(db);
	close();
	return task;
}



int ListDatabase::getUserCallback(void *data, int argc, char **argv, char **azColName)
{
	ListUser* tmp = (ListUser*) data;
	*(tmp->id) = atoi(argv[0]);
	tmp->login = argv[1];
	tmp->pass = argv[2];
	tmp->salt = argv[3];
	tmp->f_name = argv[4];
	tmp->l_name = argv[5];
	tmp->email = argv[6];
	return 0;
}



ListDatabase::ListUser ListDatabase::getUser(Text_t login)
{
	open();
	char *zErrMsg = 0;
	int rc;

	ListUser* data = new ListUser();
	*data->id = -1;
	std::ostringstream oss;
	oss << "SELECT * FROM Users WHERE Login = '" << login << "';";
	
	//std::cout << oss.str() << std::endl;
	
	rc = sqlite3_exec(db, oss.str().c_str(), getUserCallback, (void*)data, &zErrMsg);
	close();
	
	return *data;
}




/*
int main()
{
	ListDatabase x = ListDatabase("hehe");
	//x.addUser("pikaczu32", "aa", "aa", "aa", "aa", "aa");
	//auto z = x.getUser("pikaczu32");
	//cout << *z.id << "   " << z.login << "  " << z.email << std::endl;
	x.addTask("kup chleb", 1, nullptr, 0);
}*/ 



