#ifndef _LISTDATABASE_H_
#define _LISTDATABASE_H_

#include <string>
#include <vector>
#include <sqlite3.h>

#include "task.h"
class ListUser
{

};

class ListTask
{

}

class ListDatabase
{
private:
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
	
	void addUser(ListUser user);
	
	bool canChange(ListUser user, ListTask task);
	bool canFinish(ListUser user, ListTask task);
	
	void finish(ListUser user, ListTask task);
	void change(ListUser user, ListTask task, std::string description);
	
	
};




#endif