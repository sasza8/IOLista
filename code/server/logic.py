authenticatedUsers = dict()

def authenticate(username, password):
	if username == 'test' and password == 'testowa':
		authenticatedUsers['tOkEn'] = 'test'
		return 'tOkEn'
	else:
		return None

def getAuthenticatedUser(token):
	user = authenticatedUsers.get(token)
	return user