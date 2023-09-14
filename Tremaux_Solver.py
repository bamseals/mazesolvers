import World as World

import argparse
import random
import threading
import time

class Cell():
  def __init__(self, value, x, y, dfs, dfe, prev ):
    self.value: tuple = value # tuple
    self.x:int = x
    self.y:int = y
    self.dfs:int = dfs # distance from start
    self.dfe:int = dfe
    self.prev:Cell = prev # cell that this cell was discovered from

class MazeSolver(object): 
    def __init__(self, world):
        self.world = world

        self.bfs_discovered = {} # closed queue
        self.bfs_queue = [] # open queue

    def bfs_search(self):
        """ Conduct a BFS of the maze. """
        # Initialize the BFS
        self.bfs_discovered[self.world.player] = 'root'
        self.bfs_queue.append(self.world.player)

        # Set the color of the cell since it has been discovered
        self.world.set_cell_discovered(self.world.player)
 
        while len(self.bfs_queue) > 0:
            node = self.bfs_queue.pop(0)
            if self.world.check_finish_node(node):
                #end node has been found
                return node

            # If not the goal, process the cell and adjacent valid move to cells.
            self.world.set_cell_visited(node)
            for n in [(node[0]-1, node[1]), (node[0]+1, node[1]), (node[0], node[1]-1), (node[0], node[1]+1)]:
                if self.world.check_valid_move_cell(n) and n not in self.bfs_discovered:
                    self.bfs_discovered[n] = node
                    self.bfs_queue.append(n)

                    # Set the color of the cell since it has been discovered.
                    self.world.set_cell_discovered(n)
                    # Sleep in order to show the exploration.
                    # Comment line out if you want it to just go.
                    # Adjust float value lower if you want it to go faster.
                    time.sleep(0.05)

        def tremaux_search(self):
            root = Cell((self.world.player[0], self.world.player[1]))
            self.bfs_discovered[self.world.player] = 'root'
            self.bfs_queue.append(self.world.player)

    def bfs_path(self, end):
        """ Construct the path to traverse the maze. 

        Args:
            end: the ending cell to start the backwards path through.
        """
        path = [end]

        while self.bfs_discovered[path[-1]] != 'root':
            path.append(self.bfs_discovered[path[-1]])

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

        goal = self.bfs_search()
        path = self.bfs_path(goal)

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
