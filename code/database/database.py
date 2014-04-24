# -*- coding: utf-8 -*-
import MySQLdb
import itertools

#TODO: sensowne tworzenie warunkow,
#TODO: ogolny __SELECT__
#TODO: ogolny __UPDATE__


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
                tmp.append(u"%(" + unicode(i).encode("utf-8") + u")s")
        sql += u", ".join(tmp)
        sql += u");"  #sql == INSERT INTO <table_name> (<columns>) VALUES (%(column)s);
        conn = None
        conn = MySQLdb.connect(host=self._host_, user=self._user_, passwd=self._pass_, db=self._db_)
        with conn:
            cur = conn.cursor()
            cur.execute("set names utf8;")

            cur.executemany(sql, values)

    def insert_user(self, login, password, salt, first_name, last_name, email):
        vals = [dict(Login=login.encode("utf-8"),
                     Password=password.encode("utf-8"),
                     Salt=salt.encode("utf-8"),
                     FirstName=first_name.encode("utf-8"),
                     LastName=last_name.encode("utf-8"),
                     Email=email.encode("utf-8"))]
        self.__INSERT__(u"users", vals)

    def insert_task(self, description, owner, parent_id='NULL', parents='NULL', done=0, created_at=u'NOW()',
                    last_change=u'NOW()'):
        vals = [dict(Description=unicode(description).encode("utf-8"),
                     Owner=unicode(owner).encode("utf-8"),
                     ParentID=unicode(parent_id).encode("utf-8"),
                     Parents=unicode(parents).encode("utf-8"),
                     Done=unicode(done).encode("utf-8"),
                     CreatedOn=unicode(created_at).encode("utf=8"),
                     LastChange=unicode(last_change).encode("utf-8"))]
        self.__INSERT__(u"tasks", vals)

    def insert_access(self, task_id, user_id, permissions_flag):
         """
        nalezy ustalic co jaka flaga znaczy,
        mozna podawac wszystko co unicode zamieni do sensownych postaci
        task_id->bigint unsigned
        user_id->int unsigned
        permissions_flag-> int unsigned
         """
         vals = [dict(TaskID=unicode(task_id).encode("utf-8"),
                      UserID=unicode(user_id).encode("utf-8"),
                      Permissions=unicode(permissions_flag)("utf-8"))]
         self.__INSERT__(u"have_access", vals)

    def __SELECT__(self, columns, table_name, condition):
        """
        condition tuple (string z %s, slownik argumentow jak w insert)
        columns slownik
        """
        sql = u"SELECT "
        tmp = []
        for c in columns:
            tmp.append(c)
        sql += u", ".join(tmp)
        sql += u" FROM "
        sql += unicode(table_name).encode("utf-8")
        args = [dict()]
        if condition is not None:
            sql += u" WHERE "
            sql += condition[0]
            args = condition[1]
        sql += u";"
        conn = MySQLdb.connect(host=self._host_, user=self._user_, passwd=self._pass_, db=self._db_)
        z = []
        with conn:
            cur = conn.cursor()
            cur.execute("set names utf8;")
            cur.executemany(sql, args)
            z = cur.fetchall()
        return z

    def select_users(self, user_id=None, login=None, password=None, salt=None, first_name=None, last_name=None, email=None):
        """
        tuple tupli (puste jesli brak wierszy)
		robi AND podanych argumentow


        """
        columns = [unicode("*").encode("utf-8")]
        tmp = None
        con_str = u""
        str_tmp = []
        con_atrs = [dict()]
        if user_id is not None:
            str_tmp.append(u"UserID=%(con1)s".encode("utf-8"))
            con_atrs[0] = dict(dict(con1=unicode(user_id).encode("utf-8")).items() + con_atrs[0].items())
            tmp = 1
        if login is not None:
            str_tmp.append(u"Login=%(con2)s".encode("utf-8"))
            con_atrs[0] = dict(dict(con2=unicode(login).encode("utf-8")).items() + con_atrs[0].items())
            tmp = 1
        if password is not None:
            str_tmp.append(u"Password=%(con3)s".encode("utf-8"))
            con_atrs[0] = dict(dict(con3=unicode(password).encode("utf-8")).items() + con_atrs[0].items())
            tmp = 1
        if salt is not None:
            str_tmp.append(u"Salt=%(con4)s".encode("utf-8"))
            con_atrs[0] = dict(dict(con4=unicode(salt).encode("utf-8")).items() + con_atrs[0].items())
            tmp = 1
        if first_name is not None:
            str_tmp.append(u"FirstName=%(con5)s".encode("utf-8"))
            con_atrs[0] = dict(dict(con5=unicode(first_name).encode("utf-8")).items() + con_atrs[0].items())
            tmp = 1
        if last_name is not None:
            str_tmp.append(u"LastName=%(con6)s".encode("utf-8"))
            con_atrs[0] = dict(dict(con6=unicode(last_name).encode("utf-8")).items() + con_atrs[0].items())
            tmp = 1
        if email is not None:
            str_tmp.append(u"Email=%(con7)s".encode("utf-8"))
            con_atrs[0] = dict(dict(con7=unicode(email).encode("utf-8")).items() + con_atrs[0].items())
            tmp = 1
        con_str = u" AND ".join(str_tmp)
        condition = None
        if tmp is not None:
            condition = (con_str, con_atrs)

        x = self.__SELECT__(columns, u'users', condition)
        return x