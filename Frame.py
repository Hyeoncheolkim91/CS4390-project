
# File frame
fileDict = dict()  # filename mapped to (filepointer, location)
buffer = 1024
extension = ""  # file extension
f = 0  # file pointer


# This function moves the file pointer to the specified location.
def content_seek(frame_index, cur_frame):
    global f
    if frame_index < cur_frame:
        cur_frame = 0  # reset frame count
        f.seek(0)
        # "While the requested frame is higher than the current frame, increment the current frame"
    while frame_index > cur_frame:
        cur_frame += 1
        f.readline()


# This function returns the data for the next frame of the specified file.
def get_frame():
    global f
    global extension
    if extension == "txt":
        return f.readline()
    else:
        print("file extenstion is not valid")
        return None


# Serves frame
# requested_file
# requested_frame
def send_frame(requested_file, requested_frame):
    global fileDict
    global extension
    global f
    extension = requested_file.split(".")[-1]
    if requested_file not in fileDict and requested_frame == 0:
        if extension == "txt":
            f = open("serverData/" + requested_file, "rb")
        # save file and specific location into dicitionary
        fileDict[requested_file] = (f, [0])
        print("file opened: ", requested_file)

    req = fileDict[requested_file]
    f = req[0]
    cur_frame = req[1][0]
    print("File retrieved: ", req)
    # seek to the desired frame
    content_seek(requested_frame, cur_frame)
    # record the new frame in the dictionary
    req[1][0] = requested_frame + 1
    # send the frame to the renderer
    frame = get_frame()
    frame = b"Streaming\n1\n\n" + bytearray(str(frame.decode()) + "\n", 'utf-8')
    return frame
