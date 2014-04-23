from twisted.internet import protocol, reactor
import json
import logic

class ServerProtocol(protocol.Protocol):
	class LoginRequiredException(Exception):
		pass
	
	def do_authenticate(self, params):
		result = dict()
		username = params.get('username')
		password = params.get('password')
		token = logic.authenticate(username, password)
		if token is None:
			result['type'] = 'loginFailed'
		else:
			result['type'] = 'loginOK'
			result['authToken'] = token
		self.transport.write(json.dumps(result))
	
	def do_getTasks(self, params, user):
		pass
	
	def do_addTask(self, params, user):
		pass
	
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
				user = logic.getAuthenticatedUser(authToken)
				if user is None:
					raise self.LoginRequiredException()
			
				if requestType == 'getTasks':
					do_getTasks(params, user)
				if requestType == 'addTask':
					do_addTask(params, user)
		
		except self.LoginRequiredException:
			result = dict()
			result['type'] = 'loginRequired'
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