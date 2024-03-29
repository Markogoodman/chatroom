import socket
import sys
import threading

from threading import Thread

max_name_len = 10

class Client:
    def __init__(self, name):
        assert len(name) <= max_name_len, f'Length of name must < {max_name_len}'

        self.name = name
        self.server = None
        self.socket = None

    @staticmethod
    def message_handler(msg):
        msg = msg.decode('utf-8')
        name = msg[:max_name_len].strip()
        msg = msg[max_name_len:]

        return name, msg


    def message_receiver(self):
        t = threading.currentThread()
        while getattr(t, "do_run", True):
            msg = None
            try:
                name, msg = self.message_handler(self.socket.recv(1024))
                print(name + ': ' + msg)
            except Exception as ex:
                pass

    def message_sender(self):
        while True:
            try:
                msg = self.name.ljust(max_name_len)
                msg += input('')
                self.socket.send(msg.encode('utf-8'))
            except Exception as ex:
                #  down
                self.socket.close()
                sys.exit()

    def connect(self, host, port):
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.connect((host, port))
        t_sender = Thread(target=self.message_sender)
        t_receiver = Thread(target=self.message_receiver)
        # daemon thread stops when main thread stops
        t_sender.daemon = True
        t_receiver.daemon = True
        t_sender.start()
        t_receiver.start()
        t_sender.join()
        t_receiver.do_run = False

        print('Server is down')


if __name__ == '__main__':
    c = Client('pig')
    c.connect('192.168.100.11', 5566)
