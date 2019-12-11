import math
import socket
import sys
import time
import uuid
from enum import Enum

fields = {(0, 0): "C"}
location = (0, 0)

def rec_fields_ManualInput(clientsocket):
    data = clientsocket.recv(1024).decode()
    if not data:
        print("Connection closed")
        return True
    if len(data) == 50:
        print(data[0:10])
        print(data[10:20])
        print(data[20:30])
        print(data[30:40])
        print(data[40:50])
    elif len(data) == 18:
        print(data[0:6])
        print(data[6:12])
        print(data[12:18])
    elif len(data) == 98:
        print(data[0:14])
        print(data[14:28])
        print(data[28:42])
        print(data[42:56])
        print(data[56:70])
        print(data[70:84])
        print(data[84:98])
    else:
        # Lose / Win
        print(data)
        return True
    return False

def rec_fields_AlgorithmBased(clientsocket):
    data = clientsocket.recv(1024).decode()
    if not data:
        print("Connection closed")
        return True
    if len(data) >= 18:
        print("Raw: " + data)
        index_fields(data.replace(" ", ""))

    else:
        # Lose / Win
        print(data)
        return True
    return False

def index_fields(data):
    side_length = math.sqrt(len(data))
    sight_range = int(side_length/2)
    for x in range(location[0]-sight_range, location[0]+sight_range):
        for y in range(location[1]-sight_range, location[1]+sight_range):



class CommandType(Enum):
    UP = "up"
    RIGHT = "right"
    DOWN = "down"
    LEFT = "left"

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as clientsocket:
    try:
        # Verbindung herstellen (Gegenpart: accept() )
        host = "localhost" if len(sys.argv) <= 1 else sys.argv[1]
        port = 5050 if len(sys.argv) <= 2 else int(sys.argv[2])
        name = "User"+str(uuid.uuid1()) if len(sys.argv) <= 3 else sys.argv[3]
        print("Host: " + host)
        print("Port: " + str(port))
        print("Name: " + name)

        clientsocket.connect((host, port))
        clientsocket.send(name.encode())
        data = clientsocket.recv(1024).decode()

        if not data or not data == "OK":
            # Schließen, falls Verbindung geschlossen wurde
            clientsocket.close()
        else:
            msg = "up"
            while True:
                if rec_fields_AlgorithmBased(clientsocket):
                    break
                while True:
                    # Nachricht schicken
                    if msg.lower() == "up":
                        clientsocket.send(CommandType.UP.value.encode())
                        msg="down"
                        break
                    elif msg.lower() == "down":
                        clientsocket.send(CommandType.DOWN.value.encode())
                        msg="up"
                        break
                    elif msg.lower() == "left":
                        clientsocket.send(CommandType.LEFT.value.encode())
                        break
                    elif msg.lower() == "right":
                        clientsocket.send(CommandType.RIGHT.value.encode())
                        break
    except socket.error as serr:
        print("Socket error: " + serr.strerror)