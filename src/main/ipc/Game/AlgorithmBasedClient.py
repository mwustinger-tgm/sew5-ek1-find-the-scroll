import math
import random
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


class FieldType(Enum):
    GRASS = 'G'
    CASTLE = 'C'
    FOREST = 'F'
    MOUNTAIN = 'M'
    LAKE = 'L'
    BOMB = 'B'


sight_for_type = {FieldType.GRASS: 2, FieldType.CASTLE: 1, FieldType.FOREST: 1, FieldType.MOUNTAIN: 3,
                  FieldType.LAKE: 0, FieldType.BOMB: 10}

automatic = True

def move_with_command(known_spaces, current_location, command):
    x, y = current_location
    new = (x, y)

    if command == CommandType.UP:
        new = (x, y + 1)
    elif command == CommandType.DOWN:
        new = (x, y - 1)
    elif command == CommandType.LEFT:
        new = (x - 1, y)
    elif command == CommandType.RIGHT:
        new = (x + 1, y)
    if known_spaces[new] == FieldType.LAKE:
        return current_location
    else:
        return new


def index_fields(known_spaces, current_location, data):
    updated_fields = known_spaces.copy()
    side_length = math.sqrt(len(data))
    sight_range = int(side_length / 2)
    for i in range(0, len(data)):
        x = current_location[0] - sight_range + int(i % side_length)
        y = current_location[1] + sight_range - int(i / side_length)
        updated_fields[(x, y)] = FieldType(data[i])
    return updated_fields


class AlgorithmBasedClient:
    def __init__(self):
        self.my_spaces = {(0, 0): FieldType.CASTLE}
        self.my_location = (0, 0)
        self.bomb_location = None

    def rec_fields(self, clientsocket):
        data = clientsocket.recv(1024).decode()
        if not data:
            print("Connection closed")
            return True
        if len(data) >= 18:
            print("Received Raw Data: ", data)
            self.my_spaces = index_fields(self.my_spaces, self.my_location, data.replace(" ", ""))
        else:
            # Lose / Win
            print(data)
            return True
        return False

    def eval_next_step(self):
        if self.bomb_location is None:
            for x, y in self.my_spaces.keys():
                if self.my_spaces[x, y] == "B":
                    self.bomb_location = (x, y)
                    print("******Spotted the Scroll******")

        if self.bomb_location is not None:
            self.eval_path_to_scroll()
        else:
            return self.eval_most_new_spaces_found()

    def eval_path_to_scroll(self):
        vector_to_scroll = (self.bomb_location[0] - self.my_location[0], self.bomb_location[1] - self.my_location[1])
        later_used_command = random.choice(list(CommandType))
        for command in CommandType:
            tested_location = move_with_command(self.my_spaces, self.my_location, command)
            tested_vector = (self.bomb_location[0] - tested_location[0], self.bomb_location[1] - tested_location[1])
            if abs(tested_vector[0])+abs(tested_vector[1]) < abs(vector_to_scroll[0])+abs(vector_to_scroll[1]):
                later_used_command = command
        return later_used_command

    def eval_most_new_spaces_found(self):
        most_new_spaces_found = len(self.my_spaces) - 1
        later_used_command = random.choice(list(CommandType))
        for command in CommandType:
            tested_location = move_with_command(self.my_spaces, self.my_location, command)
            type_of_tested_location = self.my_spaces[tested_location]
            amt_of_spaces_found = len(index_fields(self.my_spaces, tested_location, "G" * int(
                pow(sight_for_type[type_of_tested_location] * 2 + 1, 2))))
            if most_new_spaces_found < amt_of_spaces_found:
                most_new_spaces_found = amt_of_spaces_found
                later_used_command = command
            elif most_new_spaces_found == amt_of_spaces_found:
                later_used_command = random.choice([later_used_command, command])
        return later_used_command

    def connect_to_server(self):
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as clientsocket:
            try:
                # Verbindung herstellen (Gegenpart: accept() )
                host = "localhost" if len(sys.argv) <= 1 else sys.argv[1]
                port = 5050 if len(sys.argv) <= 2 else int(sys.argv[2])
                name = "User" + str(uuid.uuid1()) if len(sys.argv) <= 3 else sys.argv[3]
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
                    while True:
                        if self.rec_fields(clientsocket):
                            break

                        print("--NEW-ROUND")
                        print("\tLocation: ", self.my_location)
                        next_step = self.eval_next_step()
                        print("\tNext Step: ", next_step.value)
                        self.my_location = move_with_command(self.my_spaces, self.my_location, next_step)
                        if not automatic:
                            msg = input("Send this step to server? (Y/n) ")
                            if msg.lower() == "n" or msg.lower() == "no" or msg.lower() == "nein":
                                break
                        clientsocket.send(next_step.value.encode())

            except socket.error as serr:
                print("Socket error: " + serr.strerror)


if __name__ == "__main__":
    c = AlgorithmBasedClient()
    c.connect_to_server()
