import sys
import os
from room import Room
from player import Player
from world import World
from util import Stack, Queue
import random
from ast import literal_eval


def find_nearest_unexplored_room(graph, current_room):
    # print("Current_room in fnur: " + str(current_room))
    unexplored_room_path = bfs(graph, current_room)
    # use below if you want to use dfs instead:
    # unexplored_room_path = dfs(graph, current_room)

    # Now convert it to directions
    # print(unexplored_room_path)
    path = []

    for i in range(0, len(unexplored_room_path) - 1):
        # print("Graph at room " +
        #       str(unexplored_room_path[i]) + ": " + str(graph[unexplored_room_path[i]]))
        graph_list = list(
            graph[unexplored_room_path[i]].items())
        direction = ''
        for entry in graph_list:
            if entry[1] == unexplored_room_path[i + 1]:
                direction = entry[0]
                # print("Direction found: " + str(direction))
        path.append(direction)
    # print(str(path))
    return(path)


def bfs(graph, starting_vertex):
    visited_vertices = set()
    queue = Queue()
    queue.enqueue([starting_vertex])
    while queue.size() > 0:
        current_path = queue.dequeue()

        current_vertex = current_path[-1]
        # print("current_vertex " + str(current_vertex))
        if current_vertex not in visited_vertices:
            neighbors = get_neighbors(graph, current_vertex)
            for neighbor in neighbors:
                new_path = list(current_path)
                new_path.append(neighbor)
                queue.enqueue(new_path)
                if neighbor == '?':
                    return new_path
            visited_vertices.add(current_vertex)


def dfs(graph, starting_vertex):
    visited_vertices = set()
    stack = Stack()
    stack.push([starting_vertex])
    while stack.size() > 0:
        current_path = stack.pop()

        current_vertex = current_path[-1]
        # print("current_vertex " + str(current_vertex))
        if current_vertex not in visited_vertices:
            neighbors = get_neighbors(graph, current_vertex)
            for neighbor in neighbors:
                new_path = list(current_path)
                new_path.append(neighbor)
                stack.push(new_path)
                if neighbor == '?':
                    return new_path
            visited_vertices.add(current_vertex)


def get_neighbors(graph, room):
    # Gets the room IDs of neighbors, or '?'
    return list(graph[room].values())


def create_traversal_path():
    visited_rooms = set()
    player = Player(world.starting_room)
    visited_rooms.add(player.current_room)
    traversal_path = []
    stack = []
    graph = dict()
    graph[player.current_room.id] = dict()
    current_exits = player.current_room.get_exits()
    for exit in current_exits:
        graph[player.current_room.id][exit] = '?'

    # Find which directions are still unexplored
    unexplored_directions = [entry[0] for entry in list(
        graph[player.current_room.id].items()) if entry[1] == '?']

    move = unexplored_directions[random.randint(
        0, len(unexplored_directions) - 1)]
    stack.append(move)

    while len(visited_rooms) < len(room_graph):
        move = stack.pop()

        # Hold on to the prev room's id to update the graph
        prev_room = player.current_room.id

        # Travel that direction
        player.travel(move)
        # print("In room " + str(player.current_room.id))

        # Log that direction
        traversal_path.append(move)

        # Add current_room to visited_rooms
        visited_rooms.add(player.current_room)
        # print("now num visited rooms is " + str(len(visited_rooms)))

        current_exits = player.current_room.get_exits()

        # Update the graph
        # Update the entry for the prev room
        graph[prev_room][move] = player.current_room.id

        # Make an entry for the current room if it's not already there
        if player.current_room.id not in graph:
            graph[player.current_room.id] = dict()
            for exit in current_exits:
                graph[player.current_room.id][exit] = '?'

        # Update the entry for the current room.
        opposites = {'n': 's', 's': 'n', 'e': 'w', 'w': 'e'}
        opposite = opposites[move]
        # print(opposite)
        graph[player.current_room.id][opposite] = prev_room
        # print("graph so far: " + str(graph))

        # Find which directions are still unexplored
        unexplored_directions = [entry[0] for entry in list(
            graph[player.current_room.id].items()) if entry[1] == '?']

        # If still has unexplored_directions,
        # Pick a random unexplored direction from the current room.
        if len(unexplored_directions) > 0:
            # To See if having a default direction decreases the traveral_path length
            # if 'w' in unexplored_directions:
            #     move = 'w'
            # else:
            move = unexplored_directions[random.randint(
                0, len(unexplored_directions) - 1)]

            # Add it to the stack
            stack.append(move)
        elif len(visited_rooms) == len(room_graph):
            # print("Traversal_path is made! " + str(traversal_path))
            return traversal_path
        else:
            # Back up to nearest room with an unexplored direction
            next_step = find_nearest_unexplored_room(
                graph, player.current_room.id)
            # print(next_step)
            for i in range(0, len(next_step) - 1):
                player.travel(next_step[i])
                # print("In room " + str(player.current_room.id))

                # Log that direction
                traversal_path.append(next_step[i])

                # Add current_room to visited_rooms
                visited_rooms.add(player.current_room)
            stack.append(next_step[-1])

# Load world and have player traverse it


# Load world
world = World()

# You may uncomment the smaller graphs for development and testing purposes.
# map_file = "maps/test_line.txt"
# map_file = "maps/test_cross.txt"
# map_file = "maps/test_loop.txt"
# map_file = "maps/test_loop_fork.txt"
map_file = "maps/main_maze.txt"

# Loads the map into a dictionary
"""
room_graph=literal_eval(open(map_file, "r").read())
"""
with open(os.path.join(sys.path[0], map_file), 'r') as f:
    room_graph = literal_eval(f.read())
world.load_graph(room_graph)

# Print an ASCII map
world.print_rooms()

player = Player(world.starting_room)

# TRAVERSAL TEST
visited_rooms = set()
player.current_room = world.starting_room
visited_rooms.add(player.current_room)

# Fill this out with directions to walk
# traversal_path = ['n', 'n']
traversal_path = create_traversal_path()

# Test, where player travels through traversal_path.
for move in traversal_path:
    player.travel(move)
    visited_rooms.add(player.current_room)

if len(visited_rooms) == len(room_graph):
    print(
        f"TESTS PASSED: {len(traversal_path)} moves, {len(visited_rooms)} rooms visited")
else:
    print("TESTS FAILED: INCOMPLETE TRAVERSAL")
    print(f"{len(room_graph) - len(visited_rooms)} unvisited rooms")


#######
# UNCOMMENT TO WALK AROUND
#######
# player.current_room.print_room_description(player)

'''
while True:
    cmds = input("-> ").lower().split(" ")
    if cmds[0] in ["n", "s", "e", "w"]:
        player.travel(cmds[0], True)
    elif cmds[0] == "q":
        break
    else:
        print("I did not understand that command.")
'''
