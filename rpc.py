from socket import socket
import pickle
import textwrap


class UnavailableLog(Exception):
    pass


class NotExistingUser(Exception):
    pass


class AlreadyExistingName(Exception):
    pass


class UnavailableFunction(Exception):
    pass


class InvalidData(Exception):
    pass


class AnonymousUser(Exception):
    pass


def rpc():

    return RPC()


class RPC:

    def __init__(self, host='localhost', port=33000):
        ADDR = (host, port)
        # BUFSIZ = 1024

        self.state = 1
        self.socket = socket()
        try:
            self.socket.connect(ADDR)
        except ConnectionRefusedError:
            pass

        self.clients = {}

    def send(self, msg):
        msg = pickle.dumps(msg)
        self.state = send_all_data(self.socket, msg)

    def recv(self):
        resp = get_all_data(self.socket)
        return resp['ok'], resp

    def add(self, a, b):
        msg = {'func': 'add', 'a': a, 'b': b}
        self.send(msg)

        ok, resp = self.recv()
        if not ok:
            raise UnavailableFunction

        return resp['data']

    def get_logs(self):
        msg = {'func': 'get_logs'}
        self.send(msg)

        ok, resp = self.recv()
        if not ok:
            raise UnavailableFunction

        return resp['data']

    def write_to_log(self, log):
        msg = {'func': 'write_to_log', 'log': log}
        self.send(msg)

        ok, resp = self.recv()
        if not ok:
            e = resp['data']['error']
            if e == 'UnavailableLog':
                raise UnavailableLog

    def write_to_client_log(self, target, log):
        msg = {'func': 'write_to_client_log', 'user': target, 'log': log}
        self.send(msg)

        ok, resp = self.recv()
        if not ok:
            e = resp['resp']['data']
            if e == 'NotExisingUser':
                raise NotExistingUser

    def set_name(self, name):
        msg = {'func': 'set_name', 'name': name}
        self.send(msg)

        ok, resp = self.recv()
        if not ok:
            e = resp['data']['error']
            if e == 'AlreadyExistingName':
                raise AlreadyExistingName

    def get_users(self):
        msg = {'func': 'get_users'}
        self.send(msg)

        ok, resp = self.recv()

        if not ok:
            raise UnavailableFunction

        return resp['data']

    def get_my_logs(self, user):
        msg = {'func': 'get_my_logs', 'user': user}
        self.send(msg)

        ok, resp = self.recv()

        if not ok:
            e = resp['data']['error']
            if e == 'AnoynmousUser':
                raise AnonymousUser

        return resp['data']

    def __repr__(self):
        text = """
            Available functions:
            int add(int a, int b): return a + b
            """
        return textwrap.dedent(text)


def get_all_data(socket):

    data = []
    while True:
        packet = socket.recv(4096)
        data.append(packet)
        if len(packet) < 4096:
            break
    data = b"".join(data)

    return pickle.loads(data)


def send_all_data(socket, msg):

    try:
        socket.send(msg)
        return 1
    except ConnectionResetError:
        return 0
    except OSError:
        return 0

