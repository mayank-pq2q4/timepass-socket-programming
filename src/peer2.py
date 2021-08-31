# import socket


# host = '127.0.0.1'
# portS = 9090

# client_skt = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# client_skt.connect((host,portS))
# msg=client_skt.recv(1024)
# msg=msg.decode('utf-8')
# print(msg)
# while True:
#  msg=input("Enter your message: \n")
#  msg=msg.encode("utf-8")
#  client_skt.sendall(msg)

# For peer to peer communication uncomment the code below:

import socket
import time
import os
from tqdm import tqdm
import _thread

HOST = '127.0.0.1' # change this to the system ipv4 address where we should recieve messages from
PORT_S = 9090
PORT_R = 8080
BUFFER_SIZE = 4096


def client():
    for i in tqdm(range(5), desc='You have 5 seconds to run the other peer program...'):
        time.sleep(1)
    filename = 'clientEcho.py'
    filesize = os.path.getsize(filename)

    client_skt = socket.socket()

    client_skt.connect((HOST, PORT_S))

    client_skt.send(f"{filename}thewall{filesize}".encode())
    progress = tqdm(range(filesize), f"Sending {filename}", unit="B", unit_scale=True, unit_divisor=1024)
    with open(filename, "rb") as file:
        while True:

            data = file.read(BUFFER_SIZE)
            if not data:
                break

            client_skt.sendall(data)
            progress.update(len(data))
    client_skt.close()

def server():

    serv_skt = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    serv_skt.bind((HOST, PORT_R))
    serv_skt.listen(1)
    print("waiting for a client...")

    connection, address = serv_skt.accept()

    # welcome_message = "Welcome to " + HOST + " at " + str(PORT_R)

    # welcome_message = welcome_message.encode('utf-8')
    # connection.send(welcome_message)

    received = connection.recv(BUFFER_SIZE).decode()

    filename, filesize = received.split("thewall")

    filename = os.path.basename(filename)

    filesize = int(filesize)
    progress = tqdm(range(filesize), f"Receiving {filename}", unit="B", unit_scale=True, unit_divisor=1024)
    with open(filename, "wb") as file:
        while True:
            data = connection.recv(BUFFER_SIZE)
            if not data:    
                break
            file.write(data)
            progress.update(len(data))
    connection.close()
    serv_skt.close()


try:
    _thread.start_new_thread(server, ())
    _thread.start_new_thread(client, ())
except:
    print("Error: unable to start thread")

while 1:
    pass

