import requests
import socket as sk

server_list = [
    'https://oru-pds-serv-prim.raah.me',
    'https://oru-pds-serv-r1.raah.me',
    'https://oru-pds-serv-r2.raah.me'
]

# Alias for http://oru-pds-serv.raah.me
host = ('localhost', 3999)

socket = sk.socket()

socket.bind(host)

while True:
    payload, client = socket.recvfrom(65536)

    for i, server in enumerate(server_list):
        try:
            requests.request()

