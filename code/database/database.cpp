
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
	//id = new UserID_t();
	id = sqlite3_last_insert_rowid(db); //!!! wywali sie przy wspolbieznosci
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
	id = sqlite3_last_insert_rowid(db); //!!! wywali sie przy wspolbieznosci
}



void ListDatabase::ListTask::insert(sqlite3* db)
{ //TODO injctions!!! 
	char *zErrMsg = 0;
	std::ostringstream oss;
	oss << "INSERT INTO Tasks (Description, Owner, ParentID, ChildCounter, Done, CreatedOn, LastChange) VALUES ('"
	<< description <<"',";
	oss << owner_id;
	oss << ",";
	if(parent_id != -1)
	{
		oss << parent_id;
		//link(parent_id);
	}
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
					TaskID_t parent_id, TaskDone_t done)
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
	(tmp->id) = atoi(argv[0]);
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
	data->id = -1;
	std::ostringstream oss;
	oss << "SELECT * FROM Users WHERE Login = '" << login << "';";
	
	//std::cout << oss.str() << std::endl;
	
	rc = sqlite3_exec(db, oss.str().c_str(), getUserCallback, (void*)data, &zErrMsg);
	close();
	
	return *data;
}


static int getTasksCallback(void *data, int argc, char **argv, char **azColName)
{
	std::vector<ListDatabase::ListTask>* tmp = (std::vector<ListDatabase::ListTask>*) data;
	
	ListDatabase::ListTask x;
	(x.id) = atoi(argv[0]);
	x.description = argv[1];
	x.owner_id = atoi(argv[2]);
	if(argv[3])
		x.parent_id = atoi(argv[3]);
	else
	{
		x.parent_id = -1;
	}
	cout << azColName[3];
	x.child_ct = atoi(argv[4]);
	x.done = atoi(argv[5]);
	
	
	//std::cout << argv[6] << "    " << argv[7] << " hehhe " << std::endl;
	x.created_on = atoi(argv[8]);
	x.last_change = atoi(argv[9]);
	
	tmp->push_back(x);
	return 0;
}
 

std::vector<ListDatabase::ListTask>* ListDatabase::getTasks(ListDatabase::ListUser user)
{
	std::vector<ListDatabase::ListTask>* to_ret = new std::vector<ListDatabase::ListTask>();

	if(user.id != -1)
		if(user.id >= 0)
		{
			open();
			char *zErrMsg = 0;
			int rc;
			std::ostringstream oss;
			oss << "SELECT *,  strftime('%s',CreatedOn ), strftime('%s',LastChange ) FROM Tasks WHERE Owner = '" << user.id << "';";
			
			
			//std::cout << oss.str() << std::endl;
			
			rc = sqlite3_exec(db, oss.str().c_str(), getTasksCallback, (void*)to_ret, &zErrMsg);
			close();
		}
	
	
	return to_ret;
	
}



std::vector<ListDatabase::ListTask>* ListDatabase::getLists(ListDatabase::ListUser user)
{
	std::vector<ListDatabase::ListTask>* to_ret = new std::vector<ListDatabase::ListTask>();

	if(user.id != -1)
		if(user.id >= 0)
		{
			open();
			char *zErrMsg = 0;
			int rc;
			std::ostringstream oss;
			oss << "SELECT *,  strftime('%s',CreatedOn ), strftime('%s',LastChange ) FROM Tasks WHERE ParentID IS NULL AND Owner = '" << user.id << "';";
			
			//std::cout << oss.str() << std::endl;
			
			rc = sqlite3_exec(db, oss.str().c_str(), getTasksCallback, (void*)to_ret, &zErrMsg);
			oss.clear();
			
			
			
			close();
		}
	
	
	return to_ret;
	
}


std::vector<ListDatabase::ListTask>* ListDatabase::getSubTasks(ListTask parent_task)
{
	std::vector<ListDatabase::ListTask>* to_ret = new std::vector<ListDatabase::ListTask>();

	if(parent_task.id != -1)
		if(parent_task.id >= 0)
		{
			open();
			char *zErrMsg = 0;
			int rc;
			std::ostringstream oss;
			oss << "SELECT *,  strftime('%s',CreatedOn ), strftime('%s',LastChange ) FROM Tasks WHERE ParentID = '" << parent_task.id << "';";
			
			//std::cout << oss.str() << std::endl;
			
			rc = sqlite3_exec(db, oss.str().c_str(), getTasksCallback, (void*)to_ret, &zErrMsg);
			oss.clear();
			
			
			
			close();
		}
	
	
	return to_ret;
	
}


std::vector<ListDatabase::ListTask>* ListDatabase::getSubTasksList(ListUser user, ListTask parent_task)
{
	std::vector<ListDatabase::ListTask>* to_ret = new std::vector<ListDatabase::ListTask>();

	if(user.id != -1)
		if(parent_task.id >= 0)
		{
			open();
			char *zErrMsg = 0;
			int rc;
			std::ostringstream oss;
			oss << "SELECT *,  strftime('%s',CreatedOn ), strftime('%s',LastChange ) FROM Tasks WHERE ParentID = '" << parent_task.id << "' AND Owner = '" << user.id << "';";
			
			//std::cout << oss.str() << std::endl;
			
			rc = sqlite3_exec(db, oss.str().c_str(), getTasksCallback, (void*)to_ret, &zErrMsg);
			oss.clear();
			
			
			
			close();
		}
		else
			return getLists(user);
	
	
	return to_ret;
	
}

/*
int main()
{
	ListDatabase x = ListDatabase("hehe");
	//x.addUser("pikaczu32", "aa", "aa", "aa", "aa", "aa");
	auto z = x.getUser("pikaczu32");
	cout << z.id << "   " << z.login << "  " << z.email << std::endl;
	
	auto vect =  x.getTasks(z);
	cout << vect->size();
	
	
	for(int i =0; i< vect->size(); ++i)
	{
		auto tmp = vect->at(i);
		cout << "bum bum " << tmp.id << "  " << tmp.description << "   " << tmp.parent_id << "   " << tmp.created_on << std::endl;
	}
	
	delete vect;
	return 0;
	
}*/



