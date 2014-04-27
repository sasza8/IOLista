# -*- coding: UTF-8 -*-?
from database import Database
import database
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


#NIE ZNAM SIE NA TYM TODO

def gen_salt():
    """
    TODO
    zwraca losowego stringa dodawanego do hasla w celu generowania silnego hasha
    """
    return "1"


def gen_hash(password, salt):
    """
    TODO
    zwraca hasha ktorego bedziemy trzymac w bazie
    """
    return password


def get_password(my_hash, salt):
    """
    TODO
    odkodowuje trzymanego w bazie hasha (tj password)
    """
    return my_hash


#
#


class DatabaseApi:
    _database_ = None

    def __init__(self, db_user='root', db_pass='root', db_host='localhost', db_name='list'):
        """
        jesli zostaly podane zle dane inne funkcje beda rzucac WrongConnectionData
        """
        self._database_ = Database(db_user, db_pass, db_host, db_name)

    def create_user(self, login, password, first_name, last_name, email):
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
            my_id = self._database_.insert_user(login=login, password=my_hash, salt=salt, first_name=first_name,
                                                last_name=last_name, email=email)
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

    def get_user(self, login, password, first_name=None, last_name=None, email=None, user_id=None):
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

        my_pass = get_password(my_hash=tmp[0]["password"], salt=tmp[0]["salt"])
        if my_pass != password:
            raise WrongData()

        if first_name != tmp[0]["first_name"]:
            raise WrongData()

        if last_name != tmp[0]["last_name"]:
            raise WrongData()

        to_ret = dict(login=tmp[0]["login"],
                      password=tmp[0]["password"],
                      first_name=tmp[0]["first_name"],
                      last_name=tmp[0]["last_name"],
                      email=tmp[0]["email"],
                      user_id=tmp[0]["user_id"])

        return to_ret

    def create_task(self, user_id, description, parent_id=None):
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
        parents = None
        if parent_id is None:
            parent_id = 'NULL'
        else:

            tmp = (self.get_tasks(user_id=user_id, task_id=parent_id))[0]["parents"]
            parents = tmp + " " + str(parent_id)
        return self._database_.insert_task(description=description, owner=user_id, parent_id=parent_id, parents=parents)

    def get_tasks(self, user_id, task_id=None, description=None, owner=None, parent_id=None, done=None, created_at=None,
                  last_change=None):
        """
        zwraca liste slownikow widocznych dla danego usera
        (
        (slownik == wiersz, etykiey jak w naglowku)

        """
        parents = None
        return self._database_.select_tasks(task_id, description, owner, parent_id, parents, done, created_at,
                                            last_change)

    def task_is_up_to_date(self, user_id, task_id, last_change):
        """
        jesli podany last_change jest mniejszy od zapisanego w bazie danych zwraca wiersz (slownik) o tym id
        w przeciwnym wypadku None
        (TODO)
        scenariusz: klient wysyla id korzenia  + swoja date zmiany do serwera
        serwer:
        tmp = task_is_up_to_date(task_id, last_change)
        if tmp is not None:
            odeslij tmp
        else:
            odeslij OK

        jesli klient otrzyma slownik powinien wysłać do servera zapytania o wszystkich synów danego taska

        NoAccess jesli uzytkownik nie mial prawa patrzec na tego taska
        """
        return None

    def update_task(self, user_id, task_id, description=None, owner=None, parent_id=None, parents=None):
        """
        aktualizuje taska o podanym id, zmienia tylko podane pola (gdy wszystko jest None nie robi nic)
        (zmiana parenta przenosi "folder"
        (TODO)
        """
        pass

    def can_edit(self, user_id, task_id):
        """
        sprawdza czy uzytkownik moze zmienic zadanie ( w tym dodac podzadanie)
        (TODO)
        """
        return True

    def can_view(self, user_id, task_id):
        """
        sprawdza czy uzytkownik moze zobaczyc zadanie ( w tym dodac podzadanie)
        (TODO)
        """
        return True