from socket import socket
import pickle
import textwrap


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

        if self.state == 1:
            req = get_all_data(self.socket)
            return req
        return None

    def add(self, a, b):
        """Suma a y b"""

        msg = {'func': 'add', 'a': a, 'b': b}
        return self.send(msg)

    def get_logs(self):
        """Obtiene los logs de marte"""

        msg = {'func': 'get_logs'}
        return self.send(msg)

    def write_to_log(self, log):
        """Escribe en los logs"""

        msg = {'func': 'write_to_log', 'log': log}
        return self.send(msg)

    def write_to_client_log(self, target, log):
        msg = {'func': 'write_to_client_log', 'user': target, 'log': log}
        return self.send(msg)

    def set_name(self, name):
        msg = {'func': 'set_name', 'name': name}
        return self.send(msg)

    def get_users(self):
        msg = {'func': 'get_users'}
        return self.send(msg)

    def get_my_logs(self, user):
        msg = {'func': 'get_my_logs', 'user': user}
        return self.send(msg)

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

