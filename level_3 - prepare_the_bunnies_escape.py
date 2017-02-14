"""
Prepare the Bunnies' Escape
===========================

You're awfully close to destroying the LAMBCHOP doomsday device 
and freeing Commander Lambda's bunny prisoners, but once 
they're free of the prison blocks, the bunnies are going to need 
to escape Lambda's space station via the escape pods as quickly 
as possible. Unfortunately, the halls of the space station are a maze 
of corridors and dead ends that will be a deathtrap for the escaping 
bunnies. Fortunately, Commander Lambda has put you in charge of a 
remodeling project that will give you the opportunity to make things 
a little easier for the bunnies. Unfortunately (again), you can't 
just remove all obstacles between the bunnies and the escape pods - 
at most you can remove one wall per escape pod path, both to maintain 
structural integrity of the station and to avoid arousing Commander 
Lambda's suspicions. 

You have maps of parts of the space station, each starting at a 
prison exit and ending at the door to an escape pod. The map is 
represented as a matrix of 0s and 1s, where 0s are passable space and 
1s are impassable walls. The door out of the prison is at the top 
left (0,0) and the door into an escape pod is at the bottom right 
(w-1,h-1). 

Write a function answer(map) that generates the length of the 
shortest path from the prison door to the escape pod, where you are 
allowed to remove one wall as part of your remodeling plans. The path 
length is the total number of nodes you pass through, counting both 
the entrance and exit nodes. The starting and ending positions are 
always passable (0). The map will always be solvable, though you may 
or may not need to remove a wall. The height and width of the map can 
be from 2 to 20. Moves can only be made in cardinal directions; no 
diagonal moves are allowed.

Languages
=========

To provide a Python solution, edit solution.py
To provide a Java solution, edit solution.java

Test cases
==========

Inputs:
    (int) maze = [[0, 1, 1, 0], [0, 0, 0, 1], [1, 1, 0, 0], [1, 1, 1, 0]]
Output:
    (int) 7

Inputs:
    (int) maze = [[0, 0, 0, 0, 0, 0], [1, 1, 1, 1, 1, 0], [0, 0, 0, 0, 0, 0], [0, 1, 1, 1, 1, 1], [0, 1, 1, 1, 1, 1], [0, 0, 0, 0, 0, 0]]
Output:
    (int) 11
"""

class World:
    """
    Class to save variables and handle the maze
    """
    def __init__(self, maze):
        self.maze = maze
        self.height = len(maze)
        self.width = len(maze[0])
        self.min_state = (0, 0)
        self.max_state = (self.height-1, self.width-1)

    def getCoord(self, i, j):
        return self.maze[i][j]

    def setCoord(self, i, j, num):
        self.maze[i][j] = num

def answer(maze):
    # Initialize world and set initial variables
    world = World(maze)
    init_state = world.min_state
    goal_state = world.max_state
    max_path_length = world.width * world.height

    # Get minimum path length without removing any wall
    min_path_length = len(BFS(init_state, goal_state, world))
    # Set to longest possible path if we did not find a path
    if min_path_length <= 0:
        min_path_length = max_path_length

    # Get list of walls that may make a shorter path when removed
    # These are walls that are next to at least two spaces
    walls_to_remove = []
    for i in range(world.height):
        for j in range(world.width):
            coord = world.getCoord(i, j)
            if coord == 1 and len(getNeighbors((i, j), world)) > 1:
                walls_to_remove.append((i, j))
    
    # Get Manhattan distance between start and goal (distance if there were no walls)
    manhattan_distance_start_goal = getManhattanDistance(init_state, goal_state) + 1

    # Compute Breadth First Search for all the maps with a wall removed
    for wall in walls_to_remove:
        # Stop if we reach the minimum possible distance
        if min_path_length <= manhattan_distance_start_goal:
            break
        # Set the chosen wall to 0
        world.setCoord(wall[0], wall[1], 0)
        # Find shortest path for the new world
        path_length = len(BFS(init_state, goal_state, world))
        # Skip if we did not find an existing path
        if path_length > 0:
            min_path_length = min(min_path_length, path_length)
        # Set the chosen wall to 1 again
        world.setCoord(wall[0], wall[1], 1)
    return min_path_length

def BFS(state0, goal, world):
    # Add initial state to the queue
    queue = [(state0, [state0])]
    visited = {}
    # Run while there are nodes in the queue
    while len(queue) > 0:
        # Pop the first state in the queue
        (current_state, current_path) = queue[0]
        queue = queue[1:]
        # Skip it if we have already visited it
        if current_state in visited:
            continue
        # Add the state to the visited nodes
        visited[current_state] = len(current_path)
        # Check if we have reached the goal and return path if we have
        if current_state == goal:
            return current_path
        # Add all neighbors of current state to queue
        for neighbor_state in getNeighbors(current_state, world):
            neighbor_path = list(current_path)
            neighbor_path.append(neighbor_state)
            queue.append((neighbor_state, neighbor_path))
    # Return empty list if no path was found from start to goal states
    return []

def getManhattanDistance(state0, state1):
    # Return minimum possible distance between two states
    return abs(state0[0] - state1[0]) + abs(state0[1] - state1[1])

def getNeighbors(state, world):
    # Return all neighbors (states next to our state) that are 0 in world
    neighbors = []
    for i in [+1, -1]:
        state0 = state[0] + i
        if state0 >= world.min_state[0] and state0 <= world.max_state[0]:
            if world.getCoord(state0, state[1]) == 0:
                neighbors.append((state0, state[1]))
        state1 = state[1] + i
        if state1 >= world.min_state[1] and state1 <= world.max_state[1]:
            if world.getCoord(state[0], state1) == 0:
                neighbors.append((state[0], state1))
    return neighbors
