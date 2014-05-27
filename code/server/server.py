from twisted.internet import protocol, reactor
import json
import logic


class ServerProtocol(protocol.Protocol):
    serverLogic = logic.logicClass()

    class LoginRequiredException(Exception):
        pass

    def do_authenticate(self, parameters):
        try:
            result = dict()
            resParameters = dict()
            username = parameters.get('username')
            password = parameters.get('password')
            token = self.serverLogic.authenticate(username, password)
            if token is None:
                result['type'] = 'loginFailed'
            else:
                result['type'] = 'loginOK'
                resParameters['authToken'] = token
                result['parameters'] = resParameters
        except Exception as e:
            result = dict()
            result['type'] = 'authenticationFailed'
            print e
        finally:
            self.transport.write(json.dumps(result))

    def do_register(self, parameters):
        try:
            result = dict()

            username = parameters.get('username')
            password = parameters.get('password')
            email = parameters.get('email')

            if self.serverLogic.register(username, password, email):
                result['type'] = 'registerOK'
            else:
                result['type'] = 'registerFailed' # tutaj mozna dorobic wyjatki na zajety email, zajetego uzytkownika, za slabe haslo itp.
        except Exception:
            result = dict()
            result['type'] = 'registerFailed'
        finally:
            self.transport.write(json.dumps(result))

    def do_getTasks(self, parameters, user):
        try:
            result = dict()
            resParameters = dict()
            parent = parameters.get('parent', None)
            tasks = self.serverLogic.getTasks(user, parent)

            result['type'] = 'tasks'
            resParameters['subtasks'] = []
            for task in tasks:
                subtask = dict()
                subtask["id"] = task["task_id"]
                subtask["name"] = task["name"]
                subtask["description"] = task["description"]
                subtask["parent"] = task["parent_id"] if task["parent_id"] is not None else -1
                subtask["done"] = task["done"]
                subtask["createdOn"] = str(task["created_at"])
                subtask["lastChange"] = str(task["last_change"])

                resParameters['subtasks'].append(subtask)
            result['parameters'] = resParameters
        except Exception:
            result = dict()
            result['type'] = 'getTasksFailed'
        finally:
            self.transport.write(json.dumps(result))

    def do_addTask(self, parameters, user):
        try:
            result = dict()
            resParameters = dict()
            name = parameters.get('name')
            description = parameters.get('description')
            parent = parameters.get('parent', None)
            task = self.serverLogic.addTask(user, name, description, parent)
            result['type'] = 'addTaskOK'
            #resParameters['asdf']="ghij"
            print task['task_id']
            resParameters['id'] = task['task_id']
            resParameters['createdOn'] = str(task['created_at'])
            result['parameters'] = resParameters
        except Exception as e:
            result = dict()
            result['type'] = 'addTaskFailed'
            print e
        finally:
            self.transport.write(json.dumps(result))

    def do_updateTask(self, parameters, user):
        try:
            result = dict()
            id = parameters.get('id')
            if id is None:
                raise Exception
            parent = parameters.get('parent')
            name = parameters.get('name')
            description = parameters.get('parent')
            self.serverLogic.updateTask(user, id, parent, name, description)
            result['type'] = 'updateTaskOK'
        except Exception:
            result = dict()
            result['type'] = 'updateTaskFailed'
        finally:
            self.transport.write(json.dumps(result))

    def do_deleteTask(self, parameters, user):
        try:
            result = dict()
            id = parameters.get('id')
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
            parameters = jsonData.get('parameters')
            authToken = jsonData.get('authToken')

            print 'pakiet %s' % requestType

            if requestType == 'authenticate':
                self.do_authenticate(parameters)
            elif requestType == 'register':
                self.do_register(parameters)
            else:
                # pakiety wymagajace autoryzacji:
                user = self.serverLogic.getAuthenticatedUserId(authToken)
                if user is None:
                    raise self.LoginRequiredException()

                if requestType == 'getTasks':
                    self.do_getTasks(parameters, user)
                if requestType == 'addTask':
                    self.do_addTask(parameters, user)
                if requestType == 'updateTask':
                    self.do_updateTask(parameters, user)
                if requestType == 'deleteTask':
                    self.do_deleteTask(parameters, user)

        except self.LoginRequiredException:
            result = dict()
            result['type'] = 'authenticationRequired'
            self.transport.write(json.dumps(result))
        except Exception as e:
            print e
        #finally:
        #    self.transport.loseConnection()


class ServerFactory(protocol.Factory):
    def buildProtocol(self, addr):
        return ServerProtocol()


if __name__ == '__main__':
    reactor.listenTCP(16661, ServerFactory())
    reactor.run()