# -*- coding: utf-8 -*-
import MySQLdb
import MySQLdb.cursors
import datetime
import _mysql_exceptions


"""
_names_ zamienia uzywane identyfikatory na nazwy kolumn w bazie danych
_inv_names_ jest odwroceniem _names_
"""

_names_ = dict(user_id=u"UserID",
               login=u"Login",
               password=u"Password",
               salt=u"Salt",
               email=u"Email",

               task_id=u"TaskId",
               description=u"Description",
               owner=u"Owner",
               done=u"Done",
               created_at=u"CreatedOn",
               last_change=u"LastChange",
               parent_id=u"ParentID",
               parents=u"Parents",

               permissions_flag=u"Permissions",
               )

_inv_names_ = dict((v, k) for k, v in _names_.iteritems())


class Condition:
    _str_ = u""
    _args_ = dict()
    _counter_ = 0
    # TODO nawiasowanie w AND i OR
    # TODO konkatenacja bylaby fajna

    def __insert__(self, **kwargs):
        i = 0
        for name, value in kwargs.items():
            if i > 0:
                raise TypeError()
            i += 1
            if name.endswith(u"__lt"):
                self._str_ += _names_[name[:-4]]
                self._str_ += u"<"
            elif name.endswith(u"__lte"):
                self._str_ += _names_[name[:-5]]
                self._str_ += u"<="
            elif name.endswith(u"__gt"):
                self._str_ += _names_[name[:-4]]
                self._str_ += u">"
            elif name.endswith(u"__gte"):
                self._str_ += _names_[name[:-5]]
                self._str_ += u">="
            else:
                self._str_ += _names_[name]
                self._str_ += u"="
            self._str_ += u"%(con" + unicode(self._counter_) + u")s"
            self._args_.update({u"con" + unicode(self._counter_): value})
            self._counter_ += 1

    def __init__(self):
        self._str_ = u""
        self._args_ = dict()
        self._counter_ = 0

    def AND(self, **kwargs):
        if self._str_ == u"":
            for name, value in kwargs.items():
                self.__insert__(**{name: value})
                self._str_ += u" AND "
            self._str_ = self._str_[:-5]
        else:
            for name, value in kwargs.items():
                self._str_ += u" AND "
                self.__insert__(**{name: value})

    def OR(self, **kwargs):
        if self._str_ == u"":
            for name, value in kwargs.items():
                self.__insert__(**{name: value})
                self._str_ += u" OR "
            self._str_ = self._str_[:-4]
        else:
            for name, value in kwargs.items():
                self._str_ += u" OR "
                self.__insert__(**{name: value})

    def get_string(self):
        return self._str_

    def get_arguments(self):
        return [self._args_]

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

    def __INSERT__(self, table_name, **kwargs):
        sql = u"INSERT INTO " + table_name.encode("utf-8") + "("
        columns = []
        for name, value in kwargs.items():
            columns.append(_names_[name])
        sql += u",".join(columns)
        sql += u") VALUES ("
        columns = []
        args = [dict()]
        i = 0
        for name, value in kwargs.items():
            columns.append(u"%(val" + unicode(i) + u")s")
            args[0].update({u"val" + unicode(i): value})
            i += 1
        sql += u", ".join(columns)
        sql += u");"  #sql == INSERT INTO <table_name> (<columns>) VALUES (%(column)s);

        try:
            conn = MySQLdb.connect(host=self._host_, user=self._user_, passwd=self._pass_, db=self._db_,
                                   use_unicode=True, charset="utf8")
        except _mysql_exceptions.OperationalError:
            raise DBConnectionError()
        except Exception as e:
            raise DBError()

        with conn:
            cur = conn.cursor()
            cur.execute("set names utf8;")
            try:
                cur.executemany(sql, args)
            except _mysql_exceptions.IntegrityError as e:
                raise DBIntegrityError(e.args[1])
            except _mysql_exceptions.DataError as e:
                raise DBIntegrityError(e.args[1])

            m_id = cur.lastrowid
        return m_id

    def insert_user(self, login, password, salt, email):
        return self.__INSERT__(u"users", login=login, password=password, salt=salt, email=email)

    def insert_task(self, description, owner, parent_id=None, parents=None, done=0, created_at=None,
                    last_change=None):
        if created_at is None:
            created_at = datetime.datetime.now()
        if last_change is None:
            last_change = created_at
        return self.__INSERT__(u"tasks", description=description, owner=owner, parent_id=parent_id, parents=parents,
                               done=done, created_at=created_at, last_change=last_change)

    def insert_access(self, task_id, user_id, permissions_flag):
        """
        nalezy ustalic co jaka flaga znaczy,
        mozna podawac wszystko co unicode zamieni do sensownych postaci
        task_id->bigint unsigned
        user_id->int unsigned
        permissions_flag-> int unsigned
        """
        return self.__INSERT__(u"have_access", task_id=task_id, user_id=user_id, permissions_flag=permissions_flag)

    def __SELECT__(self, columns, table_name, condition):
        """
        condition - instancja klasy Condition
        columns - wybierane kolumny
        """
        sql = u"SELECT "
        tmp = []
        for col in columns:
            tmp.append(col)
        sql += u", ".join(tmp)
        sql += u" FROM "
        sql += unicode(table_name).encode("utf-8")

        args = [dict()]
        if condition is not None:
            sql += u" WHERE "
            sql += condition.get_string()
            args = condition.get_arguments()
        sql += u";"
        try:
            conn = MySQLdb.connect(host=self._host_, user=self._user_, passwd=self._pass_, db=self._db_,
                                   use_unicode=True, charset="utf8", cursorclass=MySQLdb.cursors.DictCursor)
        except _mysql_exceptions.OperationalError:
            raise DBConnectionError()
        except Exception as e:
            raise DBError()
        z = []
        with conn:
            cur = conn.cursor()
            cur.execute("set names utf8;")
            cur.executemany(sql, args)
            z = cur.fetchall()

        to_ret = []
        for row in z:
            n_row = dict()
            for name, value in row.items():
                n_row.update({_inv_names_[name]: value})
            to_ret.append(n_row)
        return to_ret

    def select_users(self, user_id=None, login=None, password=None, salt=None, email=None):
        """
        zwraca liste slownikow
        """
        f_args = locals()
        columns = []
        condition = Condition()

        for name, value in f_args.items(): #TODO zrobic to ladniej w tym momencie stworzenie zmiennej przed ta petla wyjebie kod
            if name == 'self' or name == 'f_args' or name == 'columns' or name == 'condition':
                continue
            columns.append(_names_[name])
            if value is not None:
                condition.AND(**{name: value})

        if not condition.get_string():
            condition = None

        return self.__SELECT__(columns, u'users', condition)

    def select_tasks(self, task_id=None, description=None, owner=None, parent_id=None, parents=None, done=None,
                     created_at=None, last_change=None):
        """
        zwraca liste slownikow
        """
        f_args = locals()
        columns = []
        condition = Condition()

        for name, value in f_args.items(): #TODO zrobic to ladniej w tym momencie stworzenie zmiennej przed ta petla wyjebie kod
            if name == 'self' or name == 'f_args' or name == 'columns' or name == 'condition':
                continue
            columns.append(_names_[name])
            if value is not None:
                condition.AND(**{name: value})

        if not condition.get_string():
            condition = None

        return self.__SELECT__(columns, u'tasks', condition)

    def select_access(self, task_id=None, user_id=None, permissions_flag=None):
        """
        zwraca liste slownikow
        """
        f_args = locals()
        columns = []
        condition = Condition()

        for name, value in f_args.items(): #TODO zrobic to ladniej w tym momencie stworzenie zmiennej przed ta petla wyjebie kod
            if name == 'self' or name == 'f_args' or name == 'columns' or name == 'condition':
                continue
            columns.append(_names_[name])
            if value is not None:
                condition.AND(**{name: value})

        if not condition.get_string():
            condition = None

        return self.__SELECT__(columns, u'have_access', condition)

    def __UPDATE__(self, set_values, table_name, condition):
        sql = u"UPDATE "
        sql += unicode(table_name).encode("utf-8")
        sql += u" SET "
        args = [dict()]
        tmp = []
        i = 0
        for name, value in set_values.items():
            tmp.append(_names_[name] + u"=%(val" + unicode(i) + u")s")
            args[0].update({u"val" + unicode(i): value})
            i += 1
        sql += u",".join(tmp)
        if condition is not None:
            sql += u" WHERE "
            sql += condition.get_string()

            for name, value in condition.get_arguments()[0].items():
                args[0].update({name: value})

        sql += u";"
        try:
            conn = MySQLdb.connect(host=self._host_, user=self._user_, passwd=self._pass_, db=self._db_,
                                   use_unicode=True, charset="utf8")
        except _mysql_exceptions.OperationalError:
            raise DBConnectionError()
        except Exception as e:
            raise DBError()

        with conn:
            cur = conn.cursor()
            cur.execute("set names utf8;")
            cur.executemany(sql, args)

    def update_users_and(self, **kwargs):
        """
        c__<name> - wartosc bedzie w warunku (tylko AND)
        <name>__gt/lt/lte ... - nierownosc warunku
        """
        condition = Condition()
        set_vals = dict()
        for name, value in kwargs.items():
            if name.startswith("c__"):
                name = name[3:]
                condition.AND(**{name: value})
            else:
                set_vals.update({name: value})

        self.__UPDATE__(set_vals, u"users", condition)

    def update_users_or(self, **kwargs):
        """
        c__<name> - wartosc bedzie w warunku (tylko AND)
        <name>__gt/lt/lte ... - nierownosc warunku
        """
        condition = Condition()
        set_vals = dict()
        for name, value in kwargs.items():
            if name.startswith("c__"):
                name = name[3:]
                condition.OR(**{name: value})
            else:
                set_vals.update({name: value})

        self.__UPDATE__(set_vals, u"users", condition)

    def update_tasks_and(self, **kwargs):
        """
        c__<name> - wartosc bedzie w warunku (tylko AND)
        <name>__gt/lt/lte ... - nierownosc warunku
        """
        condition = Condition()
        set_vals = dict()
        for name, value in kwargs.items():
            if name.startswith("c__"):
                name = name[3:]
                condition.AND(**{name: value})
            else:
                set_vals.update({name: value})

        self.__UPDATE__(set_vals, u"tasks", condition)

    def update_tasks_or(self, parents=None, **kwargs):
        """
        c__<name> - wartosc bedzie w warunku (tylko AND)
        <name>__gt/lt/lte ... - nierownosc warunku
        """
        condition = Condition()
        set_vals = dict()
        for name, value in kwargs.items():
            if name == "parents":
                continue
            if name.startswith("c__"):
                name = name[3:]
                condition.OR(**{name: value})
            else:
                set_vals.update({name: value})
        if not condition.get_string():
            condition = None
        if parents is not None:
            if condition is None:
                condition = Condition()
            ints = parents.split()
            for i in ints:
                condition.OR(task_id=int(i))
        if condition is not None:
            self.__UPDATE__(set_vals, u"tasks", condition)

    def update_access_and(self, **kwargs):
        """
        c__<name> - wartosc bedzie w warunku (tylko AND)
        <name>__gt/lt/lte ... - nierownosc warunku
        """
        condition = Condition()
        set_vals = dict()
        for name, value in kwargs.items():
            if name.startswith("c__"):
                name = name[3:]
                condition.AND(**{name: value})
            else:
                set_vals.update({name: value})

        self.__UPDATE__(set_vals, u"have_access", condition)

    def update_access_or(self, **kwargs):
        """
        c__<name> - wartosc bedzie w warunku (tylko AND)
        <name>__gt/lt/lte ... - nierownosc warunku
        """
        condition = Condition()
        set_vals = dict()
        for name, value in kwargs.items():
            if name.startswith("c__"):
                name = name[3:]
                condition.OR(**{name: value})
            else:
                set_vals.update({name: value})

        self.__UPDATE__(set_vals, u"have_access", condition)

    def can_save(self, user_id, task_id):
        # TODO
        return True

    def can_write(self, user_id, task_id):
        # TODO
        return True

