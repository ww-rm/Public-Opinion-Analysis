import socket
import os

key = "fdjiowebg"
result_dir = "rec_results/"
s = socket.socket()
host = "123.58.210.205"
port = 1212

s.connect((host, port))
s.sendall(key.encode())

rec = "".encode()
while True:
    data = s.recv(1024)
    if not data:
        break
    rec += data

rec = rec.decode()

while rec:
    index = rec.find("&&")
    file_name = rec[:index]
    rec = rec[index+2:]
    index = rec.find("&&")
    content = rec[:index]
    rec = rec[index+2:]
    with open(result_dir+file_name, "w") as f:
        f.write(content)

