# echo-client.py

import socket

HOST = "192.168.1.105"  # IP da XIAMI
PORT = 55443  # The port used by the server

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.connect((HOST, PORT))
    s.sendall(b'{"id":1, "method":"set_power","params":["on", "smooth", 1000]}\r\n')
    data = s.recv(1024)

print(f"Received {data!r}")