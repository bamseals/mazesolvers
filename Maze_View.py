import World as World

import argparse
import random
import threading
import time

class MazeSolver(object): 
    def __init__(self, world):
        self.world = world

        self.bfs_discovered = {}
        self.bfs_queue = []

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
       
        path = []

        # Print out the path to the console.
        # Comment out if you don't need it.
        print("Path is: ", end="")
        print(path)

        # Execute the BFS path repeatedly.
        while False:
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
