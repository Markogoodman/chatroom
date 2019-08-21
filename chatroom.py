from client import Client
from server import Server
from argparse import ArgumentParser

parser = ArgumentParser()
parser.add_argument("-r", help="s: server, c: client", \
                    dest="role", default="default")
parser.add_argument("-i", help="Server ip you want to connect.", \
                    dest="host", default="default")
parser.add_argument("-p", help="port", \
                    dest="port", default="default")
parser.add_argument("-n", help="name", \
                    dest="name", default="default")
args = parser.parse_args()

if __name__ == '__main__':
    if args.role == 's':
        # server
        s = Server(args.name, '0.0.0.0', int(args.port))
        s.host_room()

    elif args.role == 'c':
        # client
        client = Client(args.name)
        client.connect(args.host, int(args.port))


