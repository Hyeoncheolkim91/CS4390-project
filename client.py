import socket
import pickle
import sys

HOST = ''
PORT = 65432

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.connect((HOST, PORT))
    conmsg = "Hi this is from client!"
    s.sendall(conmsg.encode('utf-8'))
    while True:
        val = input("Type \'list\' to see list of text files: ")
        if val == 'list':
            val = val.encode('utf-8')
            s.send(val)
            break
        else:
            print("Invalid request, please enter correctly.\n")

    data = s.recv(1024)
    data_arr = pickle.loads(data)

    for f in data_arr:
        print(f)

    val2 = input("\nEnter the file you want to stream with extension: ")
