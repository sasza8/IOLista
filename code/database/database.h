#ifndef _LISTDATABASE_H_
#define _LISTDATABASE_H_

#include <string>
#include <vector>
#include <sqlite3.h>

typedef std::string Text_t;

// Table Users
typedef int UserID_t;
const int USER_LOGIN_MAX = 100;
const int USER_PASS_MAX = 100;
const int USER_SALT_MAX = 100;
const int USER_FNAME_MAX = 100;
const int USER_LNAME_MAX = 150;
const int USER_EMAIL_MAX = 100;

// Table Tasks
typedef int TaskID_t;
const int TASK_DESC_MAX = 4000;
typedef int TaskChildCt_t;
typedef int TaskDone_t;
typedef int DateType; // timestamp 

// Table Have_access
typedef int Perm_t; 

class ListDatabase
{
public:
	class ListUser
	{
	public:
		UserID_t id;
		Text_t login;
		Text_t pass;
		Text_t salt;
		Text_t f_name;
		Text_t l_name;
		Text_t email;
		
		static int nothing(void *NotUsed, int argc, char **argv, char **azColName){return 0;};
		static int idSelect(void *NotUsed, int argc, char **argv, char **azColName);
		
		void getID(sqlite3* db); //!!! Pewnie wywali sie przy wspolbieznosci
	public:
		ListUser(){};
		ListUser(Text_t login, Text_t pass, Text_t salt,
				Text_t f_name, Text_t l_name, Text_t email) :
				id(-1), login(login), pass(pass), salt(salt), //TODO wyifowac maxy
				f_name(f_name), l_name(l_name), email(email) {}; //TODO  sprawdzic czy login juz jest
		~ListUser()
		{
		}
		
		void insert(sqlite3* db);
	};

	class ListTask
	{
	public:
		TaskID_t id;
		Text_t description;
		UserID_t owner_id;
		TaskID_t parent_id;
		TaskChildCt_t child_ct;
		TaskDone_t done;
		DateType created_on;
		DateType last_change;
		
		static int nothing(void *NotUsed, int argc, char **argv, char **azColName){return 0;};
		void getID(sqlite3* db);
		//void link(TaskID_t parent_id);
	public:
		ListTask()
		{};
		ListTask(Text_t description, UserID_t owner_id, TaskID_t parent_id, 
					TaskDone_t done) : 
					id(-1), description(description), owner_id(owner_id), 
					parent_id(parent_id), child_ct(0), done(done) {};
		
		void insert(sqlite3* db);
	};
	


public:
	ListDatabase(std::string filename);
	~ListDatabase();
	
	
	
	void open();
	void close();
	
	std::vector<ListTask> getTasks(UserID_t user_id); // zwraca wszystkie zadania utworzone przez usera
	std::vector<ListTask> getLists(UserID_t user_id); // zwraca korzenie zadan utowrzone przez usera //TODO tez z pozwoleniami
	std::vector<ListTask> getSubTasks(TaskID_t parent_task); //zwraca liste podzadan powiazana z danym zadaniem
	std::vector<ListTask> getSubTasksList(UserID_t user_id, TaskID_t parent_task);
	
	/*void updateTask(ListTask task);
	void addTask(ListTask task);
	
	std::vector<ListTask> & changedTasks(ListUser user/*, typ_daty lastUpdate); */ 
	
	ListUser addUser(Text_t login, Text_t pass, Text_t salt,
				Text_t f_name, Text_t l_name, Text_t email); //dodaje i zwraca usera
	
	ListUser getUser(Text_t login);
	
	ListTask addTask(Text_t description, UserID_t owner_id, TaskID_t parent_id, 
					TaskDone_t done);
				
	/*
	bool canChange(ListUser user, ListTask task);
	bool canFinish(ListUser user, ListTask task);
	
	void finish(ListUser user, ListTask task);
	void change(ListUser user, ListTask task, std::string description); */

		

private:
	static int getUserCallback(void *data, int argc, char **argv, char **azColName);

	std::string name;
	sqlite3* db;
};




#endif