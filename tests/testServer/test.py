import socket
import json

def connect():
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.connect( ('localhost', 16661))
    return sock

def test_register(username, password, firstname, lastname, email):
    sock = connect()
    data = dict()
    params = dict()
    data['type'] = 'register'
    params['username'] = username
    params['password'] = password
    params['firstname'] = firstname
    params['lastname'] = lastname
    params['email'] = email
    data['params'] = params
    jsondata = json.dumps(data)
    sock.send(jsondata)

    recvdata = sock.recv(1024)
    jsonrecv = json.loads(recvdata)
    print jsonrecv['type']
    sock.close()

def test_authenticate(username, password):
    sock = connect()

    data = dict()
    params = dict()

    data['type'] = 'authenticate'
    params['username'] = username
    params['password'] = password
    data['params'] = params

    jsondata = json.dumps(data)
    sock.send(jsondata)

    recvdata = sock.recv(1024)
    jsonrecv = json.loads(recvdata)
    print jsonrecv['type']

    sock.close()