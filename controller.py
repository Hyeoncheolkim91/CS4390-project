import socket


local_hostname = socket.gethostname()
# get fully qualified hostname
local_fqdn = socket.getfqdn()
# get the according IP address
ip_address = socket.gethostbyname(local_hostname)

# Creates socket for active connection to server
serverSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
serverSocket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
print("Attempting to connect to server...")
serverSocket.connect((ip_address, 40000))
print("Connected to server.")
# Creates socket for active connection to renderer
rendererSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
rendererSocket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
print("Attempting to connect to renderer...")
rendererSocket.connect((ip_address, 4444))
print("Connected to renderer.")

# Even if the command was play while streaming, it will play from the beginning
# regardless of the state of streaming.
# Play syntax: play <filename.txt>


while True:
    command = input("Enter command(list, play, resume, pause): ")
    commandSplit = command.split()
    if command.lower() == "list":
        serverSocket.send(b"List\n0\n")
        Msg = serverSocket.recv(1024).split()
        # If user input was correct, it requests list of contents from server
        # server sends list data to controller.
        # b"-1" is used for checking correction of input.
        if Msg[1] != b"-1":
            if Msg[0] == b"List" and Msg[1] == b"1":
                iterMsg = iter(Msg)
                next(iterMsg)
                next(iterMsg)
                for items in iterMsg:
                    print(items.decode('utf-8'))
            else:
                serverSocket.send(b"List\n-1")
    elif commandSplit[0].lower() == "play":
        rendererSocket.send(b"Control\n0\nPlay\n" + bytearray(commandSplit[1] + "\n", 'utf-8'))
        Msg = rendererSocket.recv(1024).split()
        if Msg[1] != b"-1":
            if Msg[0] != b"Control" or Msg[1] != b"1":
                rendererSocket.send(b"Control\n-1\nPlay")
    elif command.lower() == "pause":
        rendererSocket.send(b"Control\n0\nPause\n")
        Msg = rendererSocket.recv(1024).split()
        if Msg[1] != b"-1":
            if Msg[0] != b"Control" or Msg[1] != b"1":
                rendererSocket.send(b"Control\n-1\nPause")
    elif command.lower() == "resume":
        rendererSocket.send(b"Control\n0\nResume\n")
        Msg = rendererSocket.recv(1024).split()
        if Msg[1] != b"-1":
            if Msg[0] != b"Control" or Msg[1] != b"1":
                rendererSocket.send(b"Control\n-1\nResume")
    else:
        print("Play syntax: play <filename.txt>")
