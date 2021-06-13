import socket
import sys
import os
from new_main import main
key = "fdjiowebg"

s = socket.socket()
host = socket.gethostname()
port = 1212
s.bind(("10.7.58.158", port))

s.listen(5)

while True:
    c, addr = s.accept()
    print("连接地址：", addr)
    rev = c.recv(1024)
    if key in rev.decode():
        print("连接正确！")
    else:
        c.close()
        continue
    path = "results/" + main()
    message = ""
    for file in os.listdir(path):
        message += file
        message += "&&"
        with open(path+"/"+file) as f:
            message += f.read()
            message += "&&"
    c.sendall(message.encode())
    print("发送完毕")
    c.close()
