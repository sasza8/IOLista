import os
import sys
sys.path.append('..') # ustawiamy sciezke importu na folder code
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
            self.db_api.create_user(login=username, password=password, email=email)
            return True
        except Exception as ex:
            print ex
            return False

    def getTasks(self, user, parent):
        tasks = self.db_api.get_tasks(user_id=user,parent_id=parent)
        return tasks

    def addTask(self, user, name, description, parent):
        id = self.db_api.create_task(user_id=user, name=name, description=description, parent_id=parent)
        task = self.db_api.get_tasks(user_id=user, t_task_id=id)
        return task[0]

    def updateTask(self, user, id, parent, name, description, done):
        self.db_api.update_task(user, id, name=name, description=description, done=done)

    def deleteTask(self, user, id):
        self.db_api.delete_task(user, id)

    def changePrivileges(self, user, id, can_see, can_edit):
        id = self.db_api.get_user(user)
        self.db_api.add_permission

    def getAuthenticatedUserId(self, token):
        user = self.authenticatedUsers.get(token)
        return user
