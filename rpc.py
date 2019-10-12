from socket import AF_INET, socket, SOCK_STREAM
import pickle
import textwrap


def rpc():

    return RPC()


class RPC:

    def __init__(self):
        # Manejo estandar cliente en arquitectura client/server
        HOST = 'localhost'
        PORT = 33000
        if not PORT:
            PORT = 33000
        else:
            PORT = int(PORT)
        BUFSIZ = 1024
        ADDR = (HOST, PORT)
        self.state = 1
        self.socket = socket(AF_INET, SOCK_STREAM)
        try:
            self.socket.connect(ADDR)
        except ConnectionRefusedError:
            pass
        # Para comunicarse en marte
        self.clients = {}

    # Función de prueba: sumar a + b, retornar a + b
    def add(self, a, b):
        message = pickle.dumps({'fnc': 'add', 'a': a, 'b': b})
        self.state = send_all_data(self.socket, message)
        if self.state == 1:
            req = get_all_data(self.socket)
            return req

    # Función: Obtener los logs general en marte
    def get_logs(self):
        message = pickle.dumps({'fnc': 'get_logs'})
        self.state = send_all_data(self.socket, message)
        if self.state == 1:
            req = get_all_data(self.socket)
            return req

    # Función para escribir en los logs
    def write_to_log(self, log):
        message = pickle.dumps({'fnc': 'write_to_log', 'log': log})
        self.state = send_all_data(self.socket, message)
        if self.state == 1:
            req = get_all_data(self.socket)
            return req

    def write_to_client_log(self, target, log):
        message = pickle.dumps({'fnc': 'write_to_client_log', 'user': target, 'log': log})
        self.state = send_all_data(self.socket, message)
        if self.state == 1:
            req = get_all_data(self.socket)
            return req

    def set_name(self, name):
        message = pickle.dumps({'fnc': 'set_name', 'name': name})
        self.state = send_all_data(self.socket, message)
        if self.state == 1:
            req = get_all_data(self.socket)
            return req

    def get_users(self):
        message = pickle.dumps({'fnc': 'get_users'})
        self.state = send_all_data(self.socket, message)
        print(self.state)
        if self.state == 1:
            req = get_all_data(self.socket)
            return req

    def get_my_logs(self, user):
        message = pickle.dumps({'fnc': 'get_my_logs', 'user': user})
        self.state = send_all_data(self.socket, message)
        if self.state == 1:
            req = get_all_data(self.socket)
            return req

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

