import socket
import time
import threading

from threading import Thread

max_name_len = 10

class Server:
    def __init__(self, name, host='127.0.0.1', port=5566):
        assert len(name) <= max_name_len, f'Length of name must < {max_name_len}'
        self.name = name
        self.host = host
        self.port = port
        self.socket = None
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

    @staticmethod
    def message_handler(msg):
        msg = msg.decode('utf-8')
        name = msg[:max_name_len].strip()
        msg = msg[max_name_len:]

        return name, msg

    def message_broadcaster(self):
        while True:
            for client in self.clients:
                #print('connection:', len(self.clients))
                try:
                    msg = client.recv(1024)
                    for client in self.clients:
                        try:
                            client.send(msg)
                        except:
                            # connection lost
                            self.clients.remove(client)
                    name, msg = self.message_handler(msg)
                    print(name + ': ' + msg)
                except socket.error:
                    # non blocking msg receiver
                    pass

    def message_sender(self):
        while True:
            msg = self.name.ljust(max_name_len)
            msg += input('')
            print('You:', msg[max_name_len:])
            for client in self.clients:
                try:
                    client.send(msg.encode('utf-8'))
                except:
                    # connection lost
                    self.clients.remove(client)


    def host_room(self, max_conn=5):

        print('Server:', socket.gethostbyname(socket.gethostname()) + ':' + str(self.port))
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        try:
            self.socket.bind((self.host, self.port))
        except OSError:
            print('Incorrect host or port. Please reset it.')
            return False
        self.socket.listen(max_conn)
        self.socket.setblocking(False)
        t_sender = Thread(target=self.message_sender)
        t_broadcaster = Thread(target=self.message_broadcaster)
        t_accepter = Thread(target=self.client_accepter, args=(max_conn,))

        t_sender.start()
        t_broadcaster.start()
        t_accepter.start()


if __name__ == '__main__':
    server = Server('marko', '0.0.0.0')
    server.host_room()
