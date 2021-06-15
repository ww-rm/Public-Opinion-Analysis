import socket
import os
import logging

key = "fdjiowebg"
result_dir = "rec_results/"
LOG_FORMAT = "%(asctime)s - %(levelname)s - %(message)s"
logging.basicConfig(filename="./client.log",
                    level=logging.INFO, format=LOG_FORMAT)
s = socket.socket()
host = "123.58.210.205"
port = 1212

s.connect((host, port))
logging.info("Start connecting server, host:%s port %s" % (host, port))
s.sendall(key.encode())
logging.info("Send password")
rec = "".encode()
while True:
    data = s.recv(1024)
    if not data:
        break
    rec += data

if rec == "".encode():
    logging.warning("Password incorrect")

rec = rec.decode()

try:
    os.makedirs(result_dir)
    logging.info("Create output dorection")
except Exception as e:
    logging.info("Already exist output direction")

while rec:
    index = rec.find("&&")
    file_name = rec[:index]
    rec = rec[index+2:]
    index = rec.find("&&")
    content = rec[:index]
    rec = rec[index+2:]
    with open(result_dir+file_name, "w") as f:
        f.write(content)
        logging.info("Succes recieving file %s with length %s" %
                     (file_name, len(content)))
logging.info("Client closed")
