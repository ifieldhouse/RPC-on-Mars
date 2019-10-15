import pickle
from socket import socket, SocketType
from threading import Thread
from datetime import datetime
from collections import deque, defaultdict


class Server:

    def __init__(self, host='', port=33000):

        self.addresses = dict()
        self.log = deque()
        self.client_logs = defaultdict(deque)
        self.names = dict()
        self.addresses_by_name = dict()

        ADDR = (host, port)
        self.BUFSIZ = 1024

        self.server = socket()
        self.server.bind(ADDR)
        self.server.listen(5)

        print('Waiting for connection...')

        ACCEPT_THREAD = Thread(target=self.accept_incoming_connections)
        ACCEPT_THREAD.start()
        ACCEPT_THREAD.join()

        self.server.close()

    def accept_incoming_connections(self):
        while True:
            client, client_address = self.server.accept()
            print(f'{client.getpeername()[1]} has connected.')
            self.addresses[client] = client_address
            Thread(target=self.handle_client, args=(client,)).start()

    @staticmethod
    def send(client, msg):
        ans = pickle.dumps(msg)
        client.send(ans)

    def add(self, msg):
        result = msg['a'] + msg['b']

        return {'ok': True, 'data': result}

    def get_logs(self):
        logs = self.log

        return {'ok': True, 'data': {logs}}

    def write_to_log(self, client, log, msg):
        timestamp = datetime.now().strftime('%d/%m/%Y %H:%M:%S')

        if client not in self.names:
            return {'ok': False, 'data': {'error': 'Anonymous clients can\'t write on the log.'}}

        handle = f'<{self.names[client]}>'
        data = msg['log']

        record = f'[{timestamp}] {handle}: {data}'
        log.append(record)

        return {'ok': True}

    def write_to_server_log(self, client, msg):
        return self.write_to_log(client, self.log, msg)

    def write_to_client_log(self, client, msg):
        user = msg['user']
        if user in self.addresses_by_name:
            print(self.addresses_by_name)

            addr = self.addresses_by_name[user]
            log = self.client_logs[addr]

            return self.write_to_log(client, log, msg)

        return {'ok': False, 'data': {'error': 'This user doesn\'t exist.'}}

    def set_name(self, client, msg):
        old = self.names.get(client)
        new = msg['name']

        if new in self.names.values():
            return {'ok': False, 'data': {'error': 'This name already exists.'}}

        self.names[client] = new
        self.addresses_by_name[new] = self.addresses_by_name.pop(old, client)

        return {'ok': True}

    def get_users(self):
        users = [self.names[client] for client in self.names]

        return {'ok': True, 'data': users}

    def get_client_logs(self, msg):
        user = msg['user']
        addr = self.addresses_by_name[user]

        if user not in self.addresses_by_name:
            return {'ok': False, 'data': {'error': 'AnonymousUser'}}

        logs = self.client_logs[addr]

        return {'ok': True, 'data': logs}

    def handle_client(self, client):
        while True:
            try:
                msg = client.recv(self.BUFSIZ)
                msg = pickle.loads(msg)

                func = msg['func']

                if func == 'add':
                    ans = self.add(msg)

                elif func == 'get_logs':
                    ans = self.get_logs()

                elif func == 'write_to_log':
                    ans = self.write_to_server_log(client, msg)

                elif func == 'write_to_client_log':
                    ans = self.write_to_client_log(client, msg)

                elif func == 'set_name':
                    ans = self.set_name(client, msg)

                elif func == 'get_users':
                    ans = self.get_users()

                elif func == 'get_my_logs':
                    ans = self.get_client_logs(msg)

                self.send(client, ans)

            # El cliente se desconectó repentinamente
            except (EOFError, ConnectionResetError):
                print(f'Client {client.getpeername()[1]} disconnected.')
                client.close()
                break


if __name__ == '__main__':

    a = Server()
