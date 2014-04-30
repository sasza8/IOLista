# -*- coding: UTF-8 -*-?
from database import Database
import database
import datetime
"""
zostana dodane wyjatki tylko musze ogarnac jak sie je robi :P
aktualnie ich nie obsluguje wiec wyjatki bazy moga latac jak porabane
DatabaseError bedzie w takiej stytuacji leciec (zaimplementuje)
NoAccess jak uzytkownik (listy nie bazy) nie bedzie mial uprawnien
"""


# Exceptions
class NoAccess(Exception):
    def __init__(self):
        pass

    def __unicode__(self):
        return u"User don't have access to this Task / ID"


class DatabaseError(Exception):
    def __init__(self):
        pass

    def __unicode__(self):
        return u"Database crashed try again"


class WrongConnectionData(Exception):
    def __init__(self):
        pass

    def __unicode__(self):
        return u"Wrong db_user/db_pass/db_host/db_name, create new DatabaseApi with correct data"


class WrongData(Exception):
    def __init__(self):
        pass

    def __unicode__(self):
        return u"Can't create task/user with that data"


class LoginAlreadyInUse(WrongData):
    def __init__(self):
        pass

    def __unicode__(self):
        return u"Login already in use"


class EmailAlreadyInUse(WrongData):
    def __init__(self):
        pass

    def __unicode__(self):
        return u"Email already in use"
#
#


def gen_salt():
    import os
    salt = "".join([ chr( (ord(char)%94) + 33) for char in os.urandom(12)])
    return salt


def gen_hash(password, salt):
    import hashlib
    hash = hashlib.sha1(password+salt).hexdigest()
    return hash


class DatabaseApi:
    _database_ = None

    def __init__(self, db_user='root', db_pass='root', db_host='localhost', db_name='list'):
        """
        jesli zostaly podane zle dane inne funkcje beda rzucac WrongConnectionData
        """
        self._database_ = Database(db_user, db_pass, db_host, db_name)

    def create_user(self, login, password, email):
        """
        tworzy nowego uzytkownika i zwraca jego id
        wyjatki:
        LoginAlreadyInUse
        EmailAlreadyInUse
        WrongConnectionData - konstruktor api dostal zle dane
        DatabaseError - dzieja sie dziwne rzeczy (jak bedzie czesto latac to wejde w to glebiej
        jak pojawi sie cos innego to mowic
        """
        salt = gen_salt()
        my_hash = gen_hash(password=password, salt=salt)

        try:
            my_id = self._database_.insert_user(login=login, password=my_hash, salt=salt, email=email)
        except database.DBIntegrityError as e:
            if "Login" in e.args[0]:
                raise LoginAlreadyInUse()
            if "Email" in e.args[0]:
                raise EmailAlreadyInUse()
            raise WrongData()
        except database.DBConnectionError:
            raise WrongConnectionData()
        except:
            raise DatabaseError()

        return my_id

    def get_user(self, login, password, email=None, user_id=None):
        """
        zwraca usera
        gdy podany email login moze byc none
        zwraca None jesli uzytkownika nie ma w bazie

        """
        if login is None:
            if email is None:
                if user_id is None:
                    raise WrongData()
        try:
            tmp = self._database_.select_users(login=login, email=email, user_id=user_id)
        except database.DBConnectionError:
            raise WrongConnectionData()
        except Exception as e:
            raise DatabaseError()

        if not tmp:
            return None

        my_pass = gen_hash(password=password, salt=tmp[0]["salt"])
        if my_pass != tmp[0]["password"]:
            raise WrongData()

        to_ret = dict(login=tmp[0]["login"],
                      password=tmp[0]["password"],
                      email=tmp[0]["email"],
                      user_id=tmp[0]["user_id"])

        return to_ret

    def create_task(self, user_id, name, description=None, parent_id=None):
        """
        tworzy nowe podzadanie, zwraca jego indeks i aktualizuje baze
        wpisana data == datetime.datetime.now()
        owner powinien byc tworzacym uzytkownikiem
        uprawnienia sa dziedziczne
        (TODO)
        wyrzuci wyjatek NoAccess jesli uzytkownik nie ma prawa tworzyc
        DatabaseError jesli baza sie wywali
        WrongData jesli zostana podane bledne dane
        """


        now = datetime.datetime.now()

        task_id = self._database_.insert_task(description=description, owner=user_id, parent_id=parent_id,
                                              created_at=now, name=name)
        add_access = True
        if parent_id is not None:
            tmp = self._database_.select_access(task_id=parent_id)
            for row in tmp:
                self._database_.insert_access(task_id=task_id, user_id=row["user_id"], can_see=row["can_see"],
                                              can_edit=row["can_edit"])
                if row["user_id"] == user_id:
                    add_access = False
        if add_access:
            self._database_.insert_access(task_id=task_id, user_id=user_id, can_see=1, can_edit=1)
        return task_id

    def get_tasks(self, user_id, **kwargs):
        """
        zwraca liste taskow (jako slownik) widocznych dla danego usera
        kluczem powinny być nazwy kolumn (patrz _names_ w database.py)
        warunki:
        - funkcja robi ANDa
        - t_<kolumna> podkresla ze chodzi o tabele tasks
        - h_<kolumna> podkresla ze chodzi o tabele z uprawnieniami (to join task z uprawnieniami na miejscu userid)
        - <kolumna>__lt  - <
        - <kolumna>__lte - <=
        - <kolumna>__gt  - >
        - <kolumna>__gte - >=
        - <kolumna>      - =
        - <kolumna>__neq - !=
        (
        (slownik == wiersz, etykiey jak w datase.py _names_)
        """
        tmp = self._database_.select_tasks_user(user_id, can_see=1, **kwargs)
        return self._database_.select_tasks_user(user_id, can_see=1, **kwargs)

    def update_task(self, user_id, task_id, name=None, description=None, owner=None, parent_id="", done=None):
        """
        aktualizuje taska o podanym id, zmienia tylko podane pola (gdy wszystko jest None nie robi nic)
        (zmiana parenta przenosi "folder")
        i wlasnie tu rodzi sie problem
        co jesli user a mial dostep do "folderu" A ale nie B
        do folderu A dodalismy liste L (powiedzmy przez usera b)
        user b przenosi L z A do B
         czy user a powinien miec wciaz dostep do L?
         (aktualnie ma)
        """
        tmp = self._database_.select_access(task_id=task_id, user_id=user_id)
        now = datetime.datetime.now()
        if tmp:
            if tmp[0]["can_edit"] == 1:
                if parent_id == "":
                    self._database_.update_tasks_and(c__task_id=task_id, name=name, description=description, owner=owner,
                                                     done=done, last_change=now)
                elif parent_id is not None:
                    tmp = self._database_.select_access(task_id=parent_id, user_id=user_id)
                    if tmp:
                        if tmp[0]["can_edit"] == 1:
                            self._database_.update_tasks_and(c__task_id=task_id, name=name, description=description,
                                                             owner=owner, done=done, parent_id=parent_id, last_change=now)
                else:
                    self._database_.update_tasks_and(c__task_id=task_id, name=name, description=description,
                                                     owner=owner, done=done, parent_id=parent_id)

                if done: # rekurencyjne zakonczenie
                    tmp = self._database_.select_tasks(parent_id=task_id)
                    for row in tmp:
                        self.update_task(user_id=user_id, task_id=row["task_id"], done=done)

    def can_edit(self, user_id, task_id):
        """
        sprawdza czy uzytkownik moze zmienic zadanie ( w tym dodac podzadanie)
        (TODO)
        """
        tmp = self._database_.select_access(task_id=task_id, user_id=user_id)
        if tmp:
            if tmp[0]["can_edit"] == 1:
                return True
        return False

    def can_view(self, user_id, task_id):
        """
        sprawdza czy uzytkownik moze zobaczyc zadanie ( w tym dodac podzadanie)
        (TODO)
        """
        tmp = self._database_.select_access(task_id=task_id, user_id=user_id)
        if tmp:
            if tmp[0]["can_see"] == 1:
                return True
        return False

    def add_permission(self, task_id, user_id, can_see=1, can_edit=0):
        """
        can_edit implikuje can_see
        powiedzmy ze user a tworzy liste A
        daje userowi b dostep do listy A
        w liscie A user b dodaje liste B
        user a zabiera dostep do listy A userowi b
        czy b powinien miec dostep do D (aktualnie nie ma)
        """
        #TODO!!!!!!!!!!!!!!!!!!!!!!!!

        tmp = self._database_.select_access(task_id=task_id, user_id=user_id)
        if can_edit == 1:
            can_see = 1

        if tmp:
            self._database_.update_access_and(c__task_id=task_id, c__user_id=user_id, can_see=can_see, can_edit=can_edit)
        else:
            self._database_.insert_access(task_id=task_id, user_id=user_id, can_see=can_see)

        tmp = self._database_.select_tasks(parent_id=task_id)
        for row in tmp:
            self.add_permission(task_id=row["task_id"], user_id=user_id, can_see=can_see,can_edit=can_edit)


