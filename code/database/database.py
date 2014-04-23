# -*- coding: utf-8 -*-
import MySQLdb


class Database:
    _user_ = None
    _pass_ = None
    _host_ = None
    _db_ = None

    def __init__(self, db_user='root', db_pass='root', db_host='localhost', db_name='list'):
        self._user_ = db_user
        self._pass_ = db_pass
        self._host_ = db_host
        self._db_ = db_name

    def __INSERT__(self, table_name, values):
        sql = u"INSERT INTO " + table_name.encode("utf-8") + "("
        tmp = []
        for k in values:
            for i, j in k.iteritems():
                tmp.append(i)
        sql += u",".join(tmp)
        sql += u") VALUES ("
        tmp = []
        for k in values:
            for i, j in k.iteritems():
                tmp.append(u"%(" + str(i).encode("utf-8") + u")s")
        sql += u", ".join(tmp)
        sql += u");"  #sql == INSERT INTO <table_name> (<columns>) VALUES (%(column)s);
        conn = None
        conn = MySQLdb.connect(host=self._host_, user=self._user_, passwd=self._pass_, db=self._db_)
        cur = conn.cursor()
        cur.execute("set names utf8;")

        cur.executemany(sql, values)
        conn.commit()
        if conn:
            conn.close()
        print sql

    def insert_user(self, login, password, salt, first_name, last_name, email):
        vals = [dict(Login=login.encode("utf-8"),
                     Password=password.encode("utf-8"),
                     Salt=salt.encode("utf-8"),
                     FirstName=first_name.encode("utf-8"),
                     LastName=last_name.encode("utf-8"),
                     Email=email.encode("utf-8"))]
        self.__INSERT__(u"users", vals)

    def insert_task(self, description, owner, parent_id='NULL', parents='NULL', done=0, created_on=u'NOW()',
                    last_change=u'NOW()'):
        vals = [dict(Description=unicode(description).encode("utf-8"),
                     Owner=unicode(owner).encode("utf-8"),
                     ParentID=unicode(parent_id).encode("utf-8"),
                     Parents=unicode(parents).encode("utf-8"),
                     Done=unicode(done).encode("utf-8"),
                     CreatedOn=unicode(created_on).encode("utf=8"),
                     LastChange=unicode(last_change).encode("utf-8"))]
        self.__INSERT__(u"tasks", vals)

    def insert_access(self, task_id, user_id, permissions_flag):
         vals = [dict(TaskID=unicode(task_id).encode("utf-8"),
                      UserID=unicode(user_id).encode("utf-8"),
                      Permissions=unicode(permissions_flag)("utf-8"))]
         self.__INSERT__(u"have_access", vals)
