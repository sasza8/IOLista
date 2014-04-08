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
typedef int TaskOwner_t;
typedef int TaskParent_t;
typedef int TaskChildCt_t;
typedef int TaskDone_t;
typedef int DateType; // timestamp 

// Table Have_access
typedef int Perm_t; 

class ListDatabase
{
	
	private:
	class ListUser
	{
		UserID_t* id;
		Text_t login;
		Text_t pass;
		Text_t salt;
		Text_t f_name;
		Text_t l_name;
		Text_t email;
	public:
		ListUser(Text_t login, Text_t pass, Text_t salt,
				Text_t f_name, Text_t l_name, Text_t email) :
				id(nullptr), login(login), pass(pass), salt(salt),
				f_name(f_name), l_name(l_name), email(email) {};
		void insert(sqlite3* db);
	};

	class ListTask
	{

	};
	
	std::string name;
	sqlite3* db;
public:
	ListDatabase(std::string filename);
	~ListDatabase();
	
	
	
	void open();
	void close();
	
	std::vector<ListTask> & getTasks(ListUser user);
	std::vector<ListTask> & getSubTasks(ListTask parent_task);
	
	void updateTask(ListTask task);
	void addTask(ListTask task);
	
	std::vector<ListTask> & changedTasks(ListUser user/*, typ_daty lastUpdate*/);
	
	void addUser(Text_t login, Text_t pass, Text_t salt,
				Text_t f_name, Text_t l_name, Text_t email);
	
	bool canChange(ListUser user, ListTask task);
	bool canFinish(ListUser user, ListTask task);
	
	void finish(ListUser user, ListTask task);
	void change(ListUser user, ListTask task, std::string description);
	
	
};




#endif