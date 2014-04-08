#include <sqlite3.h>
#include <cstdio>
#include <cstring>
#include <cstdlib>
#include <iostream>
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
	if(sqlite3_open(name, &db))
		;//throw cos 
}

void ListDatabase::close()
{
	sqlite3_close(db);
}

