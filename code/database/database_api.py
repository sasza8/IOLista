# -*- coding: UTF-8 -*-?
from database import Database

"""
zostana dodane wyjatki tylko musze ogarnac jak sie je robi :P
aktualnie ich nie obsluguje wiec wyjatki bazy moga latac jak porabane
DatabaseError bedzie w takiej stytuacji leciec (zaimplementuje)
NoAccess jak urzytkownik (listy nie bazy) nie bedzie mial uprawnien
"""


class DatabaseApi:
    _database_ = None

    def __init__(self, db_user='root', db_pass='root', db_host='localhost', db_name='list'):
        """
        rzuci wyjatek WrongConnectionData jesli nie da rady sie polaczyc
        """
        self._database_ = Database(db_user, db_pass, db_host, db_name)

    def create_task(self, user_id, description, parent_id=None):
        """
        tworzy nowe podzadanie, zwraca jego indeks i aktualizuje baze
        wpisana data == datetime.datetime.now()
        owner powinien byc tworzacym urzytkownikiem
        uprawnienia sa dziedziczne
        (TODO)
        wyrzuci wyjatek NoAccess jesli urzytkownik nie ma prawa tworzyc
        DatabaseError jesli baza sie wywali
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

    def task_is_up_to_date(self,user_id, task_id, last_change):
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

        NoAccess jesli urzytkownik nie mial prawa patrzec na tego taska
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
        sprawdza czy urzytkownik moze zmienic zadanie ( w tym dodac podzadanie)
        (TODO)
        """
        return True

    def can_view(self, user_id, task_id):
        """
        sprawdza czy urzytkownik moze zobaczyc zadanie ( w tym dodac podzadanie)
        (TODO)
        """
        return True