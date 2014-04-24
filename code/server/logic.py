import os
import sys
sys.path.append('../') # ustawiamy sciezke importu na folder code
import database.database as database
import hashlib

class logicClass:
    def __init__(self):
        self.authenticatedUsers = dict()
        self.db = database.Database()

    def authenticate(self, username, password):
        users = self.db.select_users(login=username)
        if len(users) == 0:
            return None
        user = users[0]
        dbid = user[0]
        dbsalt = user[3]
        dbpass = user[2]
        passwordhash = hashlib.sha1(password+dbsalt).hexdigest()
        if dbpass != passwordhash:
            return None
        token = "".join([ chr( (ord(char)%94) + 33) for char in os.urandom(64)]) #generujemy 64 bajty i zamieniamy na drukowalne
        self.authenticatedUsers[token] = dbid
        return token

    def register(self, username, password, firstname, lastname, email):
        try:
            salt = "".join([ chr( (ord(char)%94) + 33) for char in os.urandom(12)])
            passwordhash = hashlib.sha1(password+salt).hexdigest()
            self.db.insert_user(username, passwordhash, salt, firstname, lastname, email)
            return True
        except Exception as ex:
            print ex
            return False


    def getAuthenticatedUserId(self, token):
        user = self.authenticatedUsers.get(token)
        return user