from twisted.internet import protocol, reactor
import json
import logic


class ServerProtocol(protocol.Protocol):
    serverLogic = logic.logicClass()

    class LoginRequiredException(Exception):
        pass

    def do_authenticate(self, params):
        result = dict()
        username = params.get('username')
        password = params.get('password')
        token = self.serverLogic.authenticate(username, password)
        if token is None:
            result['type'] = 'loginFailed'
        else:
            result['type'] = 'loginOK'
            result['authToken'] = token
        self.transport.write(json.dumps(result))

    def do_register(self, params):
        result = dict()

        username = params.get('username')
        password = params.get('password')
        email = params.get('email')

        if self.serverLogic.register(username, password, email):
            result['type'] = 'registerOK'
        else:
            result['type'] = 'registerFailed' # tutaj mozna dorobic wyjatki na zajety email, zajetego uzytkownika, za slabe haslo itp.

        self.transport.write(json.dumps(result))

    def do_getTasks(self, params, user):
        result = dict()
        parent = params.get('parent', None)
        tasks = self.serverLogic.getTasks(user, parent)

        result['type'] = 'tasksList'
        result['subtasks'] = []
        for task in tasks:
            subtask = dict()
            subtask["id"] = task["id"]
            subtask["description"] = task["description"]
            subtask["parent"] = task["parentId"]
            subtask["done"] = task["done"]
            subtask["createdOn"] = task["createdOn"]
            subtask["lastChange"] = task["lastChange"]

            result['subtasks'].append(subtask)

        self.transport.write(json.dumps(result))

    def do_addTask(self, params, user):
        result = dict()

        description = params.get('description')
        parent = params.get('parent', None)
        done = params.get('done', False)

        self.serverLogic.addTask(user, description, parent)

    def dataReceived(self, data):
        try:
            jsonData = json.loads(data)
            requestType = jsonData.get('type')
            params = jsonData.get('params')
            authToken = jsonData.get('authToken')

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