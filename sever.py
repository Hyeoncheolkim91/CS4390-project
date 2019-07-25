import socket
import os
import pickle

HOSTNAME = socket.gethostname()
HOST = socket.gethostbyname(HOSTNAME)
files = []
for r, d, f in os.walk(os.path.normpath('C:\\Users\\compa\\OneDrive\\바탕 화면\\opentutorials')):
    for file in f:
        if '.txt' in file:
            files.append(file)

mysock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
mysock.bind((HOST, 65432))
mysock.listen(5)
print ("Ready to serve")
conn, addr = mysock.accept()
data = conn.recv(1024)
data = data.decode('utf-8')
print(data)

dt = conn.recv(1024)
dt = dt.decode('utf-8')
if dt == "list":
    data = pickle.dumps(files)
    conn.send(data)
    for f in files:
        print(f)

