import pickle
from socket import socket

from .exceptions import *


class RPC:

    def __init__(self, host='localhost', ports=range(30000, 30011)):

        for port in ports:
            ADDR = (host, port)

            self.state = 1
            self.socket = socket()
            try:
                self.socket.connect(ADDR)
            except ConnectionRefusedError:
                continue
            else:
                break

    def send(self, msg):
        msg = pickle.dumps(msg)
        self.state = send_all_data(self.socket, msg)

    def recv(self):
        resp = get_all_data(self.socket)
        return resp['ok'], resp

    def __getattr__(self, func):
        def method(*args, **kwargs):
            msg = {'func': func, 'data': {'args': args, 'kwargs': kwargs}}
            self.send(msg)

            ok, resp = self.recv()
            if not ok:
                raise UnavailableFunction

            return resp['data']
        return method

    def __str__(self):
        methods = self.get_methods()

        all_text = ''
        for method in methods:
            f, kw = method

            text = f"{kw.pop('return').__name__} {f}" if 'return' in kw else f'void {f}'
            text += f"({', '.join(f'{v.__name__} {k}' for k, v in kw.items())})"

            all_text += f'{text}\n'

        return all_text


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

