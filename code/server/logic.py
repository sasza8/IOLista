import os
import sys
sys.path.append('../') # ustawiamy sciezke importu na folder code
import database.database_api as database_api

class logicClass:
    def __init__(self):
        self.authenticatedUsers = dict()
        self.db_api = database_api.DatabaseApi()

    def authenticate(self, username, password):
        user = self.db_api.get_user(login=username, password=password)
        if user == None:
            return None
        id = user["user_id"]
        token = "".join([ chr( (ord(char)%94) + 33) for char in os.urandom(64)]) #generujemy 64 bajty i zamieniamy na drukowalne
        self.authenticatedUsers[token] = id
        return token

    def register(self, username, password, email):
        try:
            #self.db.insert_user(username, passwordhash, salt, email)
            return True
        except Exception as ex:
            print ex
            return False


    def getAuthenticatedUserId(self, token):
        user = self.authenticatedUsers.get(token)
        return user
