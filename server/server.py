#!/usr/bin/env python3

import pickle
from socket import socket, SocketType
from threading import Thread
from datetime import datetime
from collections import deque, defaultdict
from datetime import datetime


class UnavailableLog(Exception):
    pass


class InvalidFunction(Exception):
    pass


class AnonymousUser(Exception):
    """"Anonymous users can't write into logs or read their own."""


class AnonymousRecipient(Exception):
    """Anonymous users don't have logs."""


class AlreadyExistingName(Exception):
    """There can't be two users with the same name."""


class Server:

    def __init__(self, host='', port=33000):
        ADDR = (host, port)
        self.BUFSIZ = 1024

        self.server = socket()
        self.server.bind(ADDR)
        self.server.listen(5)

        print('Waiting for connection...')

        ACCEPT_THREAD = Thread(target=self.__accept_incoming_connections)
        ACCEPT_THREAD.start()
        ACCEPT_THREAD.join()

        self.server.close()

    def __accept_incoming_connections(self):
        while True:
            client, _ = self.server.accept()
            print(f'{client.getpeername()[1]} has connected.')
            Thread(target=self.__handle_client, args=(client,)).start()

    @staticmethod
    def __send(client, msg):
        ans = pickle.dumps(msg)
        client.send(ans)

    def __handle_client(self, client):
        while True:
            try:
                msg = client.recv(self.BUFSIZ)
                msg = pickle.loads(msg)

                func = getattr(self, msg['func'])

                if func is None:
                    ans = {'ok': False, 'data': {'error': 'InvalidFunction'}}
                else:
                    ans = {'ok': True, 'data': func(*msg['data']['args'], **msg['data']['kwargs'])}

                self.__send(client, ans)

            # El cliente se desconectó repentinamente
            except (EOFError, ConnectionResetError):
                print(f'Client {client.getpeername()[1]} disconnected.')
                client.close()
                break

    @staticmethod
    def add(a: int, b: int) -> int:
        return a + b

    @staticmethod
    def mean(*args: list) -> float:
        return sum(args)/len(args)

    @staticmethod
    def palindrome(s: str) -> bool:
        return s == s[::-1]

    @staticmethod
    def fib(n: int) -> list:
        def _fib(n):
            a, b = 1, 1
            for _ in range(n):
                yield a
                a, b = b, a + b

        return list(_fib(n))

    @staticmethod
    def cartesian(A: list, B: list) -> list:
        def _cartesian(A, B):
            for i in A:
                for j in B:
                    yield A[i], B[j]

        return list(_cartesian(A, B))

    @staticmethod
    def is_substring(s: str, S: str) -> bool:
        return s in S

    @staticmethod
    def alphabetic_string(s: str) -> str:
        return ''.join(sorted(s))

    @staticmethod
    def ping():
        print('Server has been pinged!')

    @staticmethod
    def sping(s: str):
        print(f'New ping: {s}')

    @staticmethod
    def time_on_earth() -> str:
        return str(datetime.now())

    def get_methods(self):
        return [(func, getattr(self, func).__annotations__) for func in dir(self) if callable(getattr(self, func)) and not func.startswith('_')]


if __name__ == '__main__':

    import sys

    _, h, p, *_ = sys.argv

    a = Server(host=h, port=int(p))
