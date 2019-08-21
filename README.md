# chatroom
socket

Server
python3 chatroom.py -r s -p 5566 -n marko

Client
python3 chatroom.py -r c -i 192.168.100.11 -p 5566 -n monkey

optional arguments:

  -h, --help  show this help message and exit
  
  -r ROLE     s: server, c: client
  
  -i HOST     Server ip you want to connect.
  
  -p PORT     port
  
  -n NAME     name
