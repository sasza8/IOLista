# -*- coding: utf-8 -*-
import MySQLdb
import datetime
import _mysql_exceptions

#TODO: sensowne tworzenie warunkow,
#TODO: ogolny __SELECT__
#TODO: ogolny __UPDATE__


class DBIntegrityError(_mysql_exceptions.IntegrityError):
    pass


class DBConnectionError(_mysql_exceptions.OperationalError):
    pass


class DBError(Exception):
    pass


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
                if j != unicode(u'NOW()').encode("utf-8"):
                    tmp.append(u"%(" + unicode(i).encode("utf-8") + u")s")
                elif j == unicode(u'NULL').encode("utf-8"):
                    tmp.append(u'NULL')
                else:
                    tmp.append(u'NOW()')
        sql += u", ".join(tmp)
        sql += u");"  #sql == INSERT INTO <table_name> (<columns>) VALUES (%(column)s);

        try:
            conn = MySQLdb.connect(host=self._host_, user=self._user_, passwd=self._pass_, db=self._db_)
        except _mysql_exceptions.OperationalError:
            raise DBConnectionError()
        except Exception as e:
            raise DBError()

        with conn:
            cur = conn.cursor()
            cur.execute("set names utf8;")
            try:
                cur.executemany(sql, values)
            except _mysql_exceptions.IntegrityError as e:
                raise DBIntegrityError(e.args[1])
            m_id = cur.lastrowid
        return m_id

    def insert_user(self, login, password, salt, first_name, last_name, email):
        vals = [dict(Login=login.encode("utf-8"),
                     Password=password.encode("utf-8"),
                     Salt=salt.encode("utf-8"),
                     FirstName=first_name.encode("utf-8"),
                     LastName=last_name.encode("utf-8"),
                     Email=email.encode("utf-8"))]
        return self.__INSERT__(u"users", vals)

    def insert_task(self, description, owner, parent_id='NULL', parents='NULL', done=0, created_at=None,
                    last_change=None):
        if created_at is None:
            created_at = datetime.datetime.now()
        if last_change is None:
            last_change = created_at
        vals = [dict(Description=unicode(description).encode("utf-8"),
                     Owner=int(owner),
                     Done=int(done),
                     CreatedOn=created_at,
                     LastChange=last_change)]
        if parent_id != 'NULL':
            vals[0].update({'ParentID': int(parent_id)})
        if parents != 'NULL':
            vals[0].update({'Parents': unicode(parents).encode("utf-8")})
        return self.__INSERT__(u"tasks", vals)

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
         return self.__INSERT__(u"have_access", vals)

    def __SELECT__(self, columns, table_name, condition, ret_columns):
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

        to_ret = []
        for row in z:
            n_row = dict()
            for idx, val in enumerate(row):
                n_row.update({ret_columns[idx]: val})
            to_ret.append(n_row)
        return to_ret

    def select_users(self, user_id=None, login=None, password=None, salt=None, first_name=None, last_name=None,
                     email=None):
        """
        tuple of tuples


        """
        columns = [unicode("UserID").encode("utf-8"),
                   unicode("Login").encode("utf-8"),
                   unicode("Password").encode("utf-8"),
                   unicode("Salt").encode("utf-8"),
                   unicode("FirstName").encode("utf-8"),
                   unicode("LastName").encode("utf-8"),
                   unicode("Email").encode("utf-8")
                   ]
        ret_columns = [unicode("user_id").encode("utf-8"),
                       unicode("login").encode("utf-8"),
                       unicode("password").encode("utf-8"),
                       unicode("salt").encode("utf-8"),
                       unicode("first_name").encode("utf-8"),
                       unicode("last_name").encode("utf-8"),
                       unicode("email").encode("utf-8"),]
        tmp = None
        str_tmp = []
        con_args = [dict()]
        if user_id is not None:
            str_tmp.append(u"UserID=%(con1)s".encode("utf-8"))
            con_args[0] = dict(dict(con1=unicode(user_id).encode("utf-8")).items() + con_args[0].items())
            tmp = 1
        if login is not None:
            str_tmp.append(u"Login=%(con2)s".encode("utf-8"))
            con_args[0] = dict(dict(con2=unicode(login).encode("utf-8")).items() + con_args[0].items())
            tmp = 1
        if password is not None:
            str_tmp.append(u"Password=%(con3)s".encode("utf-8"))
            con_args[0] = dict(dict(con3=unicode(password).encode("utf-8")).items() + con_args[0].items())
            tmp = 1
        if salt is not None:
            str_tmp.append(u"Salt=%(con4)s".encode("utf-8"))
            con_args[0] = dict(dict(con4=unicode(salt).encode("utf-8")).items() + con_args[0].items())
            tmp = 1
        if first_name is not None:
            str_tmp.append(u"FirstName=%(con5)s".encode("utf-8"))
            con_args[0] = dict(dict(con5=unicode(first_name).encode("utf-8")).items() + con_args[0].items())
            tmp = 1
        if last_name is not None:
            str_tmp.append(u"LastName=%(con6)s".encode("utf-8"))
            con_args[0] = dict(dict(con6=unicode(last_name).encode("utf-8")).items() + con_args[0].items())
            tmp = 1
        if email is not None:
            str_tmp.append(u"Email=%(con7)s".encode("utf-8"))
            con_args[0] = dict(dict(con7=unicode(email).encode("utf-8")).items() + con_args[0].items())
            tmp = 1
        con_str = u" AND ".join(str_tmp)
        condition = None
        if tmp is not None:
            condition = (con_str, con_args)

        x = self.__SELECT__(columns, u'users', condition, ret_columns)
        return x

    def select_tasks(self, task_id=None, description=None, owner=None, parent_id=None, parents=None, done=None, created_at=None,
                     last_change=None):
        columns = [unicode("TaskId").encode("utf-8"),
                   unicode("Description").encode("utf-8"),
                   unicode("Owner").encode("utf-8"),
                   unicode("ParentID").encode("utf-8"),
                   unicode("Parents").encode("utf-8"),
                   unicode("Done").encode("utf-8"),
                   unicode("CreatedOn").encode("utf-8"),
                   unicode("LastChange").encode("utf-8"),
                   ]
        ret_columns = [unicode("task_id").encode("utf-8"),
                       unicode("description").encode("utf-8"),
                       unicode("owner").encode("utf-8"),
                       unicode("parent_id").encode("utf-8"),
                       unicode("parents").encode("utf-8"),
                       unicode("done").encode("utf-8"),
                       unicode("created_at").encode("utf-8"),
                       unicode("last_change").encode("utf-8"),
                       ]
        tmp = None
        str_tmp = []
        con_args = [dict()]
        if task_id is not None:
            str_tmp.append(u"TaskId=%(con0)s".encode("utf-8"))
            con_args[0] = dict(dict(con0=task_id).items() + con_args[0].items())
            tmp = 1
        if description is not None:
            str_tmp.append(u"Description=%(con1)s".encode("utf-8"))
            con_args[0] = dict(dict(con1=unicode(description).encode("utf-8")).items() + con_args[0].items())
            tmp = 1
        if owner is not None:
            str_tmp.append(u"Owner=%(con2)s".encode("utf-8"))
            con_args[0] = dict(dict(con2=owner).items() + con_args[0].items())
            tmp = 1
        if parent_id is not None:
            str_tmp.append(u"ParentID=%(con3)s".encode("utf-8"))
            con_args[0] = dict(dict(con3=parent_id).items() + con_args[0].items())
            tmp = 1
        if parents is not None:
            str_tmp.append(u"Parents=%(con4)s".encode("utf-8"))
            con_args[0] = dict(dict(con4=unicode(parents).encode("utf-8")).items() + con_args[0].items())
            tmp = 1
        if done is not None:
            str_tmp.append(u"Done=%(con5)s".encode("utf-8"))
            con_args[0] = dict(dict(con5=done).items() + con_args[0].items())
            tmp = 1
        if created_at is not None:
            str_tmp.append(u"CreatedOn=%(con6)s".encode("utf-8"))
            con_args[0] = dict(dict(con6=created_at).items() + con_args[0].items())
            tmp = 1
        if last_change is not None:
            str_tmp.append(u"LastChange=%(con7)s".encode("utf-8"))
            con_args[0] = dict(dict(con7=last_change).items() + con_args[0].items())
            tmp = 1
        con_str = u" AND ".join(str_tmp)
        condition = None
        if tmp is not None:
            condition = (con_str, con_args)

        x = self.__SELECT__(columns, u'tasks', condition, ret_columns)
        return x

    def select_access(self, task_id=None, user_id=None, permissions_flag=None):
        columns = [unicode("TaskID").encode("utf-8"),
                   unicode("UserID").encode("utf-8"),
                   unicode("Permissions").encode("utf-8")
                   ]
        ret_columns = [unicode("task_id").encode("utf-8"),
                       unicode("user_id").encode("utf-8"),
                       unicode("permissions_flag").encode("utf-8")
                       ]
        tmp = None
        str_tmp = []
        con_args = [dict()]
        if task_id is not None:
            str_tmp.append(u"TaskID=%(con1)s".encode("utf-8"))
            con_args[0] = dict(dict(con1=unicode(task_id).encode("utf-8")).items() + con_args[0].items())
            tmp = 1
        if user_id is not None:
            str_tmp.append(u"UserID=%(con2)s".encode("utf-8"))
            con_args[0] = dict(dict(con2=unicode(user_id).encode("utf-8")).items() + con_args[0].items())
            tmp = 1
        if permissions_flag is not None:
            str_tmp.append(u"Permissions=%(con3)s".encode("utf-8"))
            con_args[0] = dict(dict(con3=unicode(permissions_flag).encode("utf-8")).items() + con_args[0].items())
            tmp = 1
        con_str = u" AND ".join(str_tmp)
        condition = None
        if tmp is not None:
            condition = (con_str, con_args)

        x = self.__SELECT__(columns, u'users', condition, ret_columns)
        return x

    def __UPDATE__(self, columns, values, condition):
        return -1

    def can_save(self, user_id, task_id):
        # TODO
        return True

    def can_write(self, user_id, task_id):
        # TODO
        return True

