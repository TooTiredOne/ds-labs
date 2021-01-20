import socket
import os
import tqdm
import sys

# reading args from console
filename = sys.argv[1]
HOST = sys.argv[2]
PORT = int(sys.argv[3])
SEPARATOR = "<<--->>"  # used to separate filename from filesize in the 1st messaged sent to server
BUFFER_SIZE = 4096
filesize = os.path.getsize(filename)  # obtaining the size of the file

# sending file to the server using TCP
with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
    sock.connect((HOST, PORT))  # connecting to the server
    sock.send(f"{filename}{SEPARATOR}{filesize}".encode())  # sending filename and filesize
    with open(filename, 'rb') as file:
        bread = file.read(BUFFER_SIZE)  # reading bytes from the file
        bar = tqdm.tqdm(range(filesize))  # initializing the progress bar
        while bread:
            sock.sendall(bread)  # sending bytes that we read to the server
            bread = file.read(BUFFER_SIZE)  # reading next bytes
            bar.update(len(bread))  # updating the progress bar
