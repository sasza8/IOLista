import socket
import json

def connect():
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.connect( ('localhost', 16661))
    return sock

def test_register(username, password, firstname, lastname, email):
    sock = connect()
    data = dict()
    parameters = dict()
    data['type'] = 'register'
    parameters['username'] = username
    parameters['password'] = password
    parameters['email'] = email
    data['parameters'] = parameters
    jsondata = json.dumps(data)
    sock.send(jsondata)

    recvdata = sock.recv(1024)
    jsonrecv = json.loads(recvdata)
    print jsonrecv['type']
    sock.close()

def test_authenticate(username, password):
    sock = connect()

    data = dict()
    parameters = dict()

    data['type'] = 'authenticate'
    parameters['username'] = username
    parameters['password'] = password
    data['parameters'] = parameters

    jsondata = json.dumps(data)
    sock.send(jsondata)

    recvdata = sock.recv(1024)
    jsonrecv = json.loads(recvdata)
    print jsonrecv['type']

    sock.close()