from room import Room
from util import Stack
import random
import math


class World:
    def __init__(self):
        self.starting_room = None
        self.rooms = {}
        self.room_grid = []
        self.grid_size = 0
        self.current_room = None
        self.previous_room = None

    def load_graph(self, room_graph):
        num_rooms = len(room_graph)
        rooms = [None] * num_rooms
        grid_size = 1
        for i in range(0, num_rooms):
            x = room_graph[i][0][0]
            grid_size = max(
                grid_size, room_graph[i][0][0], room_graph[i][0][1])
            self.rooms[i] = Room(
                f"Room {i}", f"({room_graph[i][0][0]},{room_graph[i][0][1]})", i, room_graph[i][0][0], room_graph[i][0][1])
        self.room_grid = []
        grid_size += 1
        self.grid_size = grid_size
        for i in range(0, grid_size):
            self.room_grid.append([None] * grid_size)
        for room_id in room_graph:
            room = self.rooms[room_id]
            self.room_grid[room.x][room.y] = room
            if 'n' in room_graph[room_id][1]:
                self.rooms[room_id].connect_rooms(
                    'n', self.rooms[room_graph[room_id][1]['n']])
            if 'e' in room_graph[room_id][1]:
                self.rooms[room_id].connect_rooms(
                    'e', self.rooms[room_graph[room_id][1]['e']])
            if 's' in room_graph[room_id][1]:
                self.rooms[room_id].connect_rooms(
                    's', self.rooms[room_graph[room_id][1]['s']])
            if 'w' in room_graph[room_id][1]:
                self.rooms[room_id].connect_rooms(
                    'w', self.rooms[room_graph[room_id][1]['w']])
        self.starting_room = self.rooms[0]

    def get_direction_of_room(self, room, current_room):
        exits = current_room.get_exits()
        direction = None
        for exit in exits:
            if current_room.get_room_in_direction(exit) is room:
                direction = exit
        return direction

    def helper_function(self, node, visited, path, prev=None):
        # this takes you back
        if node not in visited:
            # add direction to path
            direction = self.get_direction_of_room(node, prev)
            path.append(direction)
            # mark new room as visited
            visited.append(node)
            # get the new room's neighbors
            exits = node.get_exits()
            neighbors = []
            print("I am in room " + str(node.id))
            for exit in exits:
                neighbors.append(node.get_room_in_direction(exit))
            for neighbor in neighbors:
                self.helper_function(neighbor, visited, path, node)
            direction = self.get_direction_of_room(prev, node)
            path.append(direction)

    def traverse_maze(self):
        # set up empty containers
        visited = []
        node = self.starting_room
        path = []
        # add the first node to visited
        visited.append(node)
        # getting the neighbors
        exits = node.get_exits()
        neighbors = []
        for exit in exits:
            neighbors.append(node.get_room_in_direction(exit))
        # loop over neighbors calling helper function
        for neighbor in neighbors:
            self.helper_function(neighbor, visited, path, node)
        return path


    def print_rooms(self):
        rotated_room_grid = []
        for i in range(0, len(self.room_grid)):
            rotated_room_grid.append([None] * len(self.room_grid))
        for i in range(len(self.room_grid)):
            for j in range(len(self.room_grid[0])):
                rotated_room_grid[len(self.room_grid[0]) -
                                  j - 1][i] = self.room_grid[i][j]
        print("#####")
        str = ""
        for row in rotated_room_grid:
            all_null = True
            for room in row:
                if room is not None:
                    all_null = False
                    break
            if all_null:
                continue
            # PRINT NORTH CONNECTION ROW
            str += "#"
            for room in row:
                if room is not None and room.n_to is not None:
                    str += "  |  "
                else:
                    str += "     "
            str += "#\n"
            # PRINT ROOM ROW
            str += "#"
            for room in row:
                if room is not None and room.w_to is not None:
                    str += "-"
                else:
                    str += " "
                if room is not None:
                    str += f"{room.id}".zfill(3)
                else:
                    str += "   "
                if room is not None and room.e_to is not None:
                    str += "-"
                else:
                    str += " "
            str += "#\n"
            # PRINT SOUTH CONNECTION ROW
            str += "#"
            for room in row:
                if room is not None and room.s_to is not None:
                    str += "  |  "
                else:
                    str += "     "
            str += "#\n"
        print(str)
        print("#####")

