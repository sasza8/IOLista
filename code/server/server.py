from twisted.internet import protocol, reactor
import json
import logic


class ServerProtocol(protocol.Protocol):
    serverLogic = logic.logicClass()

    class LoginRequiredException(Exception):
        pass

    def do_authenticate(self, params):
        try:
            result = dict()
            username = params.get('username')
            password = params.get('password')
            token = self.serverLogic.authenticate(username, password)
            if token is None:
                result['type'] = 'loginFailed'
            else:
                result['type'] = 'loginOK'
                result['authToken'] = token
        except Exception:
            result = dict()
            result['type'] = 'authenticationFailed'
        finally:
            self.transport.write(json.dumps(result))

    def do_register(self, params):
        try:
            result = dict()

            username = params.get('username')
            password = params.get('password')
            email = params.get('email')

            if self.serverLogic.register(username, password, email):
                result['type'] = 'registerOK'
            else:
                result['type'] = 'registerFailed' # tutaj mozna dorobic wyjatki na zajety email, zajetego uzytkownika, za slabe haslo itp.
        except Exception:
            result = dict()
            result['type'] = 'registerFailed'
        finally:
            self.transport.write(json.dumps(result))

    def do_getTasks(self, params, user):
        try:
            result = dict()
            parent = params.get('parent', None)
            tasks = self.serverLogic.getTasks(user, parent)

            result['type'] = 'tasksList'
            result['subtasks'] = []
            for task in tasks:
                subtask = dict()
                subtask["id"] = task["task_id"]
                subtask["description"] = task["description"]
                subtask["parent"] = task["parent_id"]
                subtask["done"] = task["done"]
                subtask["createdOn"] = task["created_at"]
                subtask["lastChange"] = task["last_change"]

                result['subtasks'].append(subtask)
        except Exception:
            result = dict()
            result['type'] = 'getTasksFailed'
        finally:
            self.transport.write(json.dumps(result))

    def do_addTask(self, params, user):
        try:
            result = dict()
            name = params.get('name')
            description = params.get('description')
            parent = params.get('parent', None)
            task = self.serverLogic.addTask(user, name, description, parent)
            result['type'] = 'addTaskOK'
            result['id'] = task['id']
            result['craeatedOn'] = task['createdOn']
        except Exception:
            result = dict()
            result['type'] = 'addTaskFailed'
        finally:
            self.transport.write(json.dumps(result))

    def do_updateTask(self, params, user):
        try:
            result = dict()
            id = params.get('id')
            if id is None:
                raise Exception
            parent = params.get('parent')
            name = params.get('name')
            description = params.get('parent')
            self.serverLogic.updateTask(user, id, parent, name, description)
            result['type'] = 'updateTaskOK'
        except Exception:
            result = dict()
            result['type'] = 'updateTaskFailed'
        finally:
            self.transport.write(json.dumps(result))

    def do_deleteTask(self, params, user):
        try:
            result = dict()
            id = params.get('id')
            if id is None:
                raise Exception
            self.serverLogic.deleteTask(user, id)
        except Exception:
            result = dict()
            result['type'] = 'deleteTaskFailed'
        finally:
            self.transport.write(json.dumps(result))

    def dataReceived(self, data):
        try:
            jsonData = json.loads(data)
            requestType = jsonData.get('type')
            params = jsonData.get('params')
            authToken = jsonData.get('authToken')

            print 'pakiet %s' % requestType

            if requestType == 'authenticate':
                self.do_authenticate(params)
            elif requestType == 'register':
                self.do_register(params)
            else:
                # pakiety wymagajace autoryzacji:
                user = self.serverLogic.getAuthenticatedUserId(authToken)
                if user is None:
                    raise self.LoginRequiredException()

                if requestType == 'getTasks':
                    self.do_getTasks(params, user)
                if requestType == 'addTask':
                    self.do_addTask(params, user)
                if requestType == 'updateTask':
                    self.do_updateTask(params, user)
                if requestType == 'deleteTask':
                    self.do_deleteTask(params, user)

        except self.LoginRequiredException:
            result = dict()
            result['type'] = 'authenticationRequired'
            self.transport.write(json.dumps(result))
        except Exception as e:
            print e
        finally:
            self.transport.loseConnection()


class ServerFactory(protocol.Factory):
    def buildProtocol(self, addr):
        return ServerProtocol()


if __name__ == '__main__':
    reactor.listenTCP(16661, ServerFactory())
    reactor.run()