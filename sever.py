import os
import select
import socket
from Frame import send_frame

local_hostname = socket.gethostname()
# get fully qualified hostname
local_fqdn = socket.getfqdn()
# get the according IP address
ip_address = socket.gethostbyname(local_hostname)

# Create list default directory
# Put files you wish to stream into the directory..

list = os.listdir("serverData")
print(list)
print("The number of text file items: ", len(list))
listMsg = "List \n1\n"
for item in list:
    listMsg += "\n" + item
print(listMsg)

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
sock.bind((ip_address, 40000))
sock.listen(5)
# list to put incoming sockets
Sockets = [sock]

while True:
    # select.select is used for multiplexing of I/O
    # Instead of using timeout, we used select.select to make connection in ready state
    # server make connection whenever client or renderer tries to connect to server.
    # and different port numbers are assigned to each socket connection.
    conn_read, conn_write, conn_exception = select.select(Sockets, [], [])
    for cur in conn_read:
        # if the choice was new incoming connection
        if cur is sock:
            (newsock, newaddr) = sock.accept()
            Sockets.append(newsock)
            print("new connection")
        # if the choice was a message.
        else:
            r = cur.recv(1024)
            # if there is no message, delete the current socket object.
            if len(r) < 1:
                Sockets.remove(cur)
                print("new socket deleted")
                continue

            words = r.split(b'\n')
            # all message
            if len(words) < 2:
                print("not enough message")
                continue
            # if we get a list request, respond with our default directory
            if words[0] == b"List":
                if words[1] == b"0":
                    cur.send(str.encode(listMsg))
                    print("Served List Requested")
            # if
            elif words[0] == b"Streaming":
                # we only handle requests.
                if words[1] == b"0":
                    # stream requests have to have 4 headers
                    if len(words) < 4:
                        print("Received meassage was too short)")
                        cur.send(b"Streaming\n-1")
                        continue
                    # extract filename and frame headers.
                    requestedFile = words[2].decode()
                    requestedFrame = int(words[3])
                    # printing frames from the serve_frame.py
                    if requestedFile in list:
                        frame = send_frame(requestedFile, requestedFrame)
                        print("Sending frames: ", frame)
                        cur.send(frame)
                    else:
                        print("Requested file not found: " + requestedFile)
                        cur.send(b"Streaming\n-1")
                elif words[1] != b"-1":
                    cur.send(b"Streaming\n-1")
                    print("invalid streaming message: ", r)
            else:
                print("Invalid message: ", r)
