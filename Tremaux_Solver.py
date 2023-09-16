import World as World

import argparse
import random
import threading
import time

class Cell():
  def __init__(self, value):
    self.value: tuple = value # tuple
    self.marks: int = 0
    self.isJunction: bool = False

class MazeSolver(object): 
    def __init__(self, world):
        self.world = world
        self.discovered = {}
        self.path = []
        self.currentcell = Cell((-1,-1))

    def tremaux_search(self):
        start = Cell((self.world.player[0], self.world.player[1]))
        self.world.set_cell_discovered(self.world.player)
        self.currentcell = start
        self.discovered[start.value] = start

        while self.currentcell != 0:
            time.sleep(0.05)
            if self.world.check_finish_node(self.currentcell.value):
                return self.currentcell
            
            x = self.currentcell.value[0]
            y = self.currentcell.value[1]

            print(self.currentcell.value)

            self.currentcell.marks += 1
            if not self.currentcell.isJunction:
                if (self.currentcell.marks < 2):
                    self.world.set_cell_discovered(self.currentcell.value)
                else:
                    self.world.set_cell_visited(self.currentcell.value)

            neighbors = []
            for n in [(x+1, y), (x, y+1), (x-1, y), (x, y-1)]:
                if self.world.check_valid_move_cell(n):
                    if n in self.discovered:
                        neighbors.append(self.discovered[n])
                    else:
                        neighbors.append(Cell(n))
            
            # if somehow you are trapped in a cell with nowhere to go, end the program
            if len(neighbors) < 1:
                self.currentcell = 0
            else:
                if len(neighbors) > 2:
                    self.currentcell.isJunction = True
                    self.world.set_cell_junction(self.currentcell.value)

                next = min(neighbors, key=lambda x: x.marks)
                self.discovered[next.value] = next
                self.currentcell = next
    
    def follow_path(self):
        for key in self.discovered:
            print(key)
            print(self.discovered[key].value)
            print(self.discovered[key].marks)
        start = Cell((self.world.player[0], self.world.player[1]))
        self.path.append(start.value)
        self.currentcell = start

        x = self.currentcell.value[0]
        y = self.currentcell.value[1]

        while self.currentcell != 0:
            if self.world.check_finish_node(self.currentcell.value):
                self.path.append(self.currentcell.value)
                return self.path

            next = 0
            for n in [(x+1, y), (x, y+1), (x-1, y), (x, y-1)]:
                if n in self.discovered and self.discovered[n].marks == 1:
                    next = self.discovered[n]
                    self.path.append(n)
            self.currentcell = next

        return self.path.reverse()

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

        self.tremaux_search()
        path = self.follow_path()

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
