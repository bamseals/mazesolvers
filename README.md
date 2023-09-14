## Get Started

You can run the default solver by the following command:

`python Maze_Solver.py`

For the full assignment, generating and then solving a maze takes the following steps:
1. `python maze_generator.py --width=15 --height=15 --start_x=0 --start_y=0 --goal_x=4 --goal_y=0 --output_file="test.dat"`
2. `python Maze_Solver.py --world_file="test.dat"`
python Astar_Solver.py --world_file="maze1.dat"

You can replace `test.dat` with whatever world filename you choose.  It also allows you to generate multiple world files and store them in the folder.

Read on for additional information about each of the files as needed.   

## Generate the Maze

`python maze_generator.py --width=15 --height=15 --start_x=0 --start_y=0 --goal_x=4 --goal_y=0`

A shell of the maze generator can be seen in this file.  You will need to enhance this in order to generate valid mazes.

## Solve the Maze

`python Maze_Solver.py --world_file="demo_maze_generator.dat"`

World files are stored in the `worlds` folder located in the same directory.

Maze_Solver is where you should code your search.  I have provided a breadth first search (BFS) implementation to get you started with interacting with the World object in `World.py`.  Note that you can change the BFS implementation to a DFS implementation by removing one character in the file.

The function `set_cell_discovered` in `World.py` allows you to set the color of a cell to one that is discovered as in the BFS algorithm.  If you would like to have two or more colors, for instance in a `visited, in queue to visit` as some algorithms prefer you can either extend this function to have an additional argument for a different color, use the other `set_cell` functions, or you could create a second function.  Feel free to use the tkinter colors at (http://www.science.smith.edu/dftwiki/index.php/Color_Charts_for_TKinter)[http://www.science.smith.edu/dftwiki/index.php/Color_Charts_for_TKinter] if you would like to use a different color pallette.  

The naive BFS implementation shows the process of exploration by showing what is in the discovered queue with a green color, sky blue are visited, and the red cells are the path the agent takes in moving to the goal.  

## Maze File Specification

`x_width:15
y_width:15
x_player_start:0
y_player_start:0
walls
1, 0
1, 1
specials
4, 0, green, 1, False`

File specification isn't the most efficient, but it is explicit.  Walls are tuples of (x,y) coordinates, one per line.  For the maze there is only one exit specified on the line after `specials`.  