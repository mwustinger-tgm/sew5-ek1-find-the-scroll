import math
import socket
import sys
import time
import uuid
from enum import Enum

class CommandType(Enum):
    UP = "up"
    RIGHT = "right"
    DOWN = "down"
    LEFT = "left"

class AlgorithmBasedClient:
    def __init__(self):
        self.fields = {(0, 0): "C"}
        self.location = (0, 0)

    def rec_fields(self, clientsocket):
        data = clientsocket.recv(1024).decode()
        if not data:
            print("Connection closed")
            return True
        if len(data) >= 18:
            print("Raw: " + data)
            self.index_fields(data.replace(" ", ""))

        else:
            # Lose / Win
            print(data)
            return True
        return False

    def index_fields(self, data):
        side_length = math.sqrt(len(data))
        sight_range = int(side_length/2)
        for x in range(self.location[0] - sight_range, self.location[0] + sight_range):
            for y in range(self.location[1] - sight_range, self.location[1] + sight_range):
                print("Test")

    def connect_to_server(self):
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
                        if self.rec_fields(clientsocket):
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

if __name__=="main":
    c = AlgorithmBasedClient()
    c.connect_to_server()