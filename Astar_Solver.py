import World as World

import argparse
import random
import threading
import time

finish_coords = (-1,-1)

class Cell():
  def __init__(self, value, dfs, prev):
    global finish_coords
    self.value: tuple = value # tuple
    self.dfs:int = dfs # distance from start
    self.dfe:int = abs(value[0]-finish_coords[0]) + abs(value[1]-finish_coords[1])
    self.td:int = self.dfs + self.dfe # total distance weight
    self.prev:Cell or int = prev # cell that this cell was discovered from

class MazeSolver(object): 
    def __init__(self, world):
        self.world = world

        self.closed_queue = [] # closed queue
        self.open_queue = [] # open queue

        self.currentcell = Cell((-1,-1),0,0)

    def astar_search(self):
        global finish_coords
        finish_coords = self.world.find_finish_node()
        start = Cell((self.world.player[0], self.world.player[1]), 0, 0)

        self.open_queue.append(start)

        self.world.set_cell_discovered(self.world.player)
        self.currentcell = start

        while len(self.open_queue) > 0:
            if self.world.check_finish_node(self.currentcell.value):
                #end node has been found
                return self.currentcell

            x = self.currentcell.value[0]
            y = self.currentcell.value[1]
            
            directions = [(x-1, y), (x, y-1), (x+1, y), (x, y+1)]
            random.shuffle(directions)

            newneighbors = []
            for n in directions:
                if self.world.check_valid_move_cell(n) and not any(x.value == n for x in self.closed_queue):
                    newcell = Cell(n,self.currentcell.dfs+1,self.currentcell)
                    newneighbors.append(newcell)
                    self.open_queue.append(newcell)
                    self.world.set_cell_discovered(n)
                    time.sleep(0.1)

            self.closed_queue.append(self.currentcell)
            self.world.set_cell_visited(self.currentcell.value)
            self.open_queue.remove(self.currentcell)

            if len(newneighbors) < 1:
                closest = min(self.open_queue, key=lambda x: x.td)
                self.currentcell = closest
            else:
                closest = min(newneighbors, key=lambda x: x.td)
                self.currentcell = closest

    def astar_path(self, end):
        loop = True
        node = end
        path = []
        while loop == True:
            path.append(node.value)
            if node.prev == 0:
                loop = False
            else:
                node=node.prev

        path.reverse()
        return path

    def do_action(self,action):
        s = self.world.player
        if action == 0:
            self.world.try_move(0, -1)
        elif action == 1:
            self.world.try_move(0, 1)
        elif action == 2:
            self.world.try_move(-1, 0)
        elif action == 3:
            self.world.try_move(1, 0)
        else:
            return
        s2 = self.world.player
        return s, s2

    def run(self):

        time.sleep(1)
        t = 1

        goal = self.astar_search()
        path = self.astar_path(goal)

        # Print out the path to the console.
        # Comment out if you don't need it.
        print("Path is: ", end="")
        print(path)

        # Execute the BFS path repeatedly.
        while True:
            for i in range(len(path)-1):
                # Find which direction the player should move.
                direction = [path[i+1][0] - path[i][0], path[i+1][1] - path[i][1]]

                action = 0
                if direction[0] == 0:
                    if direction[1] == -1:
                        # up
                        action = 0
                    else:
                        # down
                        action = 1
                else:
                    if direction[0] == -1:
                        # left
                        action = 2
                    else:
                        # right
                        action = 3

                s = self.world.player
                (s, s2) = self.do_action(action)

                # Check if the game has restarted
                t += 1.0

                if self.world.has_restarted():
                    time.sleep(2)
                    self.world.restart_game()
                    if self.world.has_restarted():
                        print(f"Maze Solved in {t} steps.")
                    t = 1.0

                # MODIFY THIS SLEEP IF THE GAME IS GOING TOO FAST.
                time.sleep(0.1)

# Get command line arguments needed for the algorithm.
parser = argparse.ArgumentParser()
parser.add_argument("--world_file", type=str, default="world_enhanced.dat", help="World file in the worlds folder to use.")
args = parser.parse_args()

# Create a world to render the maze visually and allow 
# for maze exploration.
world = World.World(args.world_file)

# Create an instance of your maze solver. 
# The default is a breadth first search.
solver = MazeSolver(world)

# The solver is threaded separate from the graphics
# since graphics run in an infinite loop.
t = threading.Thread(target=solver.run)
t.daemon = True
t.start()

# Start the graphics loop.
world.start_game()
