from socket import AF_INET, socket, SOCK_STREAM
from threading import Thread
import pickle
from datetime import datetime


class Server:

    # Iniciación de conexión
    def __init__(self, host='', port=33000):

        # Comunicación en Marte
        self.addresses = {}
        self.log = ""
        self.client_logs = {}
        self.names = {}
        self.addresses_by_name = {}


        # Manejo estandar de servidor con varios clientes

        ADDR = (host, port)
        self.BUFSIZ = 1024

        self.server = socket(AF_INET, SOCK_STREAM)
        self.server.bind(ADDR)
        self.server.listen(5)

        print("Waiting for connection...")

        ACCEPT_THREAD = Thread(target=self.accept_incoming_connections)
        ACCEPT_THREAD.start()
        ACCEPT_THREAD.join()

        self.server.close()

    # Aceptar todas las conexiones
    def accept_incoming_connections(self):
        while True:
            client, client_address = self.server.accept()
            print(f"{client.getpeername()[1]} has connected.")
            self.addresses[client] = client_address
            self.client_logs[client] = ""
            Thread(target=self.handle_client, args=(client,)).start()

    @staticmethod
    def send(client, msg):
        ans = pickle.dumps(msg)
        client.send(ans)

    def add(self, msg):
        return msg['a'] + msg['b']

    def get_logs(self):
        return self.log

    def write_to_log(self, client, msg):
        timestamp = datetime.now().strftime('%d/%m/%Y %H:%M:%S')
        handle = f'<{self.names[client]}>' if client in self.names else '<Anon>'
        record = msg['log']
        self.log += f'\n[{timestamp}] {handle}: {record}'

        return True

    def write_to_client_log(self, client, msg):
        timestamp = datetime.now().strftime('%d/%m/%Y %H:%M:%S')
        user = msg['user']
        record = msg['log']

        if user in self.addresses_by_name:
            handle = f'<{self.names[client]}>' if client in self.names else '<Anon>'
            print(self.addresses_by_name)

            self.client_logs[self.addresses_by_name[user]] += f'\n[{timestamp}] {handle}: {record}'

        return True

    def set_name(self, client, msg):
        old_name = None

        if client in self.names:
            old_name = self.names[client]

        self.names[client] = msg['name']

        if old_name == None:
            self.addresses_by_name[msg['name']] = client
        elif old_name in self.addresses_by_name:
            self.addresses_by_name[msg['name']] = self.addresses_by_name.pop(old_name)

        return True

    def get_users(self):
        # answer = ''
        # for client in self.names:
        #     answer += f"{self.names[client]}\n"

        return '\n'.join(self.names[client] for client in self.names)

    def get_my_logs(self, msg):
        user = msg['user']
        ans = self.client_logs[self.addresses_by_name[user]] if user in self.addresses_by_name else "NOT FOUND"

        print(ans)

        return(ans)

    # Manejo de un cliente
    def handle_client(self, client):
        while True:
            try:
                msg = client.recv(self.BUFSIZ)
                msg = pickle.loads(msg)

                if msg['fnc'] == 'add':
                    ans = self.add(msg)

                elif msg['fnc'] == 'get_logs':
                    ans = self.get_logs()

                elif msg['fnc'] == 'write_to_log':
                    ans = self.write_to_log(client, msg)

                elif msg['fnc'] == 'write_to_client_log':
                    ans = self.write_to_client_log(client, msg)

                elif msg['fnc'] == 'set_name':
                    ans = self.set_name(client, msg)

                elif msg['fnc'] == 'get_users':
                    ans = self.get_users()

                elif msg['fnc'] == 'get_my_logs':
                    ans = self.get_my_logs(msg)

                self.send(client, ans)

            # El cliente se desconectó repentinamente
            except EOFError:
                print(f"Client {client.getpeername()[1]} disconnected.")
                client.close()
                break

            # El cliente se desconectó repentinamente
            except ConnectionResetError:
                print(f"Client {client.getpeername()[1]} disconnected.")
                client.close()
                break


if __name__ == '__main__':

    a = Server()
