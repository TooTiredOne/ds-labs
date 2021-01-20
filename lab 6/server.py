import os
import socket

HOST = '0.0.0.0'  # listening to on every ip
PORT = 8080  # port of the server

SEPARATOR = "<<--->>"  # used to separate filename from filesize in the 1st messaged sent to server
BUFFER_SIZE = 4096


def update_name(filename):
    """
    Checks if a file with given filename exists
    If so, returns filename_copy<number>

    :param filename: string
    :return: string (needed name of the file)
    """
    # list of files in the current dir
    files = os.listdir(".")
    # checks if file with the given name exists
    if filename in files:
        # if so, update its name as many times as needed by increasing the number of the end
        new_filename = filename + "_copy1"

        while new_filename in files:
            n_str = new_filename.split("_copy")[-1]
            n_num = int(n_str) + 1
            new_filename = new_filename[:-len(n_str)] + str(n_num)

        return new_filename

    return filename


# acquiring the file from the client and saving it to file system
with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as lsock:
    lsock.bind((HOST, PORT))  # binding
    lsock.listen()  # listening
    while True:
        conn, addr = lsock.accept()  # socket and address of the client
        with conn:
            # acquiring filename and filesize
            metadata = conn.recv(BUFFER_SIZE).decode()
            filename, filesize = metadata.split(SEPARATOR)[0], metadata.split(SEPARATOR)[1]
            filename = os.path.basename(filename)
            filename = update_name(filename)  # updating filename if needed
            filesize = int(filesize)

            # writing file to hosts file system
            with open(filename, 'wb') as file:
                bread = conn.recv(BUFFER_SIZE)
                while bread:
                    file.write(bread)
                    bread = conn.recv(BUFFER_SIZE)
