import time
import socket
import threading

local_hostname = socket.gethostname()
# get fully qualified hostname
local_fqdn = socket.getfqdn()
# get the according IP address
ip_address = socket.gethostbyname(local_hostname)

# Create a socket that actively connects to the server
serverSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
serverSocket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
print("Connecting to server...")
serverSocket.connect((ip_address, 40000))
print("Connected to server. Now awaiting client controller...")

# Create a socket that passively listens for incoming connections on port 4444
controllerListener = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
# use Re-use option to bind in case of Time_wait
controllerListener.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
controllerListener.bind((ip_address, 4444))
controllerListener.listen(1)
# Accepts an incoming connection
controllerSocket, controllerAddress = controllerListener.accept()
print("Client controller connected.")
buffer = 1024
line_number = 0
streaming_file = False
file_name = b""

stream = ""


def cmd_from_controller():
    global line_number
    global streaming_file
    global file_name
    global controllerSocket
    while True:
        controller_input = controllerSocket.recv(buffer).split(b'\n')

        # Send back an error message to the controller for any List messages
        if controller_input[0] == b"List":
            controllerSocket.send(b"List\n-1\n")
            continue

        # Send back an error message to the controller for any Stream messages
        if controller_input[0] == b"Streaming":
            controllerSocket.send(b"Streaming\n-1\n")
            continue

        # if client inputs play
        if controller_input[0] == b"Control":
            # Send an error message if receiving a Control confirmation
            if controller_input[1] != b"0":
                controllerSocket.send(b"Control\n-1\n")
                continue

            # Pause the renderer
            if controller_input[2] == b"Pause":
                streaming_file = False
                controllerSocket.send(b"Control\n1\n")

            # Resume the renderer with the current file
            elif controller_input[2] == b"Resume":
                streaming_file = True
                controllerSocket.send(b"Control\n1\n")

            # The renderer should now be playing something
            elif controller_input[2] == b"Play":
                # renderer will play from the start even if the state was streaming or not.
                # Send controller confirmation and use third index for filename
                controllerSocket.send(b"Control\n1\n")
                file_name = controller_input[3]
                line_number = 0
                # Begin streaming from server
                streaming_file = True


def send_to_server():
    global line_number
    global streaming_file
    global file_name
    global serverSocket
    global stream
    while True:

        if streaming_file and file_name.decode().split(".")[1] == "txt":
            # To make server to see current flow of data
            serverSocket.send(b"Streaming\n0\n" + file_name + b"\n" + bytearray(str(line_number) + "\n", 'utf-8'))
            file_contents = serverSocket.recv(buffer).decode('utf-8')
            # print(file_contents)
            # line by line
            file_contents = file_contents.split("\n")
            line_number += 1
            if len(file_contents) >= 4 and len(file_contents[3]) >= 1:
                output = ""
                for i in range(3, len(file_contents)):
                    output += file_contents[i]
                print(output)
                # Give time to read each line by 1 sec
                time.sleep(1)
            else:
                streaming_file = False
                print("************************************    THE END    ************************************")


# multi-threading for get input from both server side and controller side.

threading.Thread(target=cmd_from_controller).start()
threading.Thread(target=send_to_server).start()
