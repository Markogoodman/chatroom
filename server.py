import socket
import time

from threading import Thread


class Server:
    def __init__(self, name, host='127.0.0.1', port=55):
        self.name = name
        self.host = host
        self.port = port
        self.clients = []

    def set_name(self, name):
        self.name = name

    def set_host(self, host):
        self.host = host

    def set_port(self, port):
        self.port = port

    def client_accepter(self, max_conn):
        while True:
            if len(self.clients) >= max_conn:
                time.sleep(2)
                continue
            try:
                client, address = self.socket.accept()
                self.clients.append(client)
            except:
                pass

    def message_broadcaster(self):
        while True:
            for client in self.clients:
                msg = None
                try:
                    msg = client.recv(1024).decode('utf-8')
                    print(msg)
                except socket.error:
                    pass
                for client in self.clients:
                    client.send(msg.encode('utf-8'))

    def message_sender(self):
        while True:
            msg = input('Message: ')
            if msg == '/host':
                print('Server:', socket.gethostbyname(socket.gethostname()) + ':' +  str(self.port))

            for client in self.clients:
                client.send(msg.encode('utf-8'))

    def host_room(self, max_conn=5):
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        try:
            self.socket.bind((self.host, self.port))
        except OSError:
            print('Incorrect host or port. Please reset it.')
            return Fasle
        self.socket.listen(max_conn)
        self.socket.setblocking(False)
        t_sender = Thread(target=self.message_sender)
        t_broadcaster = Thread(target=self.message_broadcaster)
        t_accepter = Thread(target=self.client_accepter, args=(max_conn,))

        t_sender.start()
        t_broadcaster.start()
        t_accepter.start()
        #self.client_accepter(max_conn)
        print('Server:', socket.gethostbyname(socket.gethostname()) + ':' + str(self.port))


server = Server('marko')
server.host_room()
'''
host = '127.0.0.1'
port = 9990
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind((host, port))
s.listen(5) # max conn

while True:
    print('Start listening')
    client, address = s.accept()
    print(client, address)
    msg = 'Hi'
    client.send(msg.encode('utf-8'))

    print(client.recv(1024).decode('utf-8'))
    client.close()

s.bind(('127.0.0.1', 111))
'''