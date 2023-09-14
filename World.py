""" Heavily adapted from World.py originally available at: https://github.com/AI4EDUC/ai-tools/tree/master/q_learning_demo """
__author__ = 'jared'
import random

from world_spec import WorldSpec

from tkinter import *

class World(object):

    def __init__(self,world_file):
        self.tk = Tk()
        self.tk.title("Maze Exploration")

        self.world_spec = WorldSpec(world_file)

        # Parameters to configure the graphics.
        self.Width = 800 // self.world_spec.x_width

        self.grid_cells = {} # Dictionary to hold references to cells in the grid.

        # Parameters to configure the world
        (self.x, self.y) = (self.world_spec.x_width, self.world_spec.y_width) # Width and height of world
        self.player = (self.world_spec.x_player_start, self.world_spec.y_player_start) # Player starting location for initial start.

        self.actions = ["up", "down", "left", "right"]

        self.board = Canvas(self.tk, width=self.x*self.Width, height=self.y*self.Width)
        self.restart = False

        # Render the world and start the experiment.
        self.render_grid()    

        self.tk.bind("<Up>", self.call_up)
        self.tk.bind("<Down>", self.call_down)
        self.tk.bind("<Right>", self.call_right)
        self.tk.bind("<Left>", self.call_left)

        self.me = self.board.create_rectangle(self.player[0]*self.Width+self.Width*2/10, self.player[1]*self.Width+self.Width*2/10,
                                    self.player[0]*self.Width+self.Width*8/10, self.player[1]*self.Width+self.Width*8/10, fill="orange", width=1, tag="me")

        self.board.grid(row=0, column=0)

    def check_finish_node(self, location):
        """ Check if the provided location tuple is a finish node. """
        return [location[0], location[1], "green", 1, False] in self.world_spec.specials
    
    def find_finish_node(self):
        finish = self.world_spec.specials[0]
        return (finish[0], finish[1])

    def check_valid_move_cell(self, location):
        """ Check if the provided location tuple is a valid cell to move to. """
        return location not in self.world_spec.walls and 0 <= location[0] < self.x and 0 <= location[1] < self.y

    def set_cell_discovered(self, location):
        """ Set the color of the cell to one denoting that it has been discovered.  Helps visualize the search. 

        Args:
            location: tuple of (x,y) coordinate.
        """
        self.board.itemconfig(self.grid_cells[location], fill='sea green')

    def set_cell_visited(self, location):
        """ Set the color of the cell to one denoting that it has been discovered.  Helps visualize the search. 

        Args:
            location: tuple of (x,y) coordinate.
        """
        self.board.itemconfig(self.grid_cells[location], fill='sky blue')     

    def set_cell_traversed(self, location):
        """ Set the color of the cell to one denoting that it has been discovered.  Helps visualize the search. 

        Args:
            location: tuple of (x,y) coordinate.
        """
        self.board.itemconfig(self.grid_cells[location], fill='sienna1')            

    def render_grid(self):
        """ Render the board """
        for i in range(self.world_spec.x_width):
            for j in range(self.world_spec.y_width):
                self.grid_cells[(i,j)] = self.board.create_rectangle(i*self.Width, j*self.Width, (i+1)*self.Width, (j+1)*self.Width, fill="white", width=1)
        for spec in self.world_spec.specials:
            cell = self.board.create_rectangle(spec[0]*self.Width, spec[1]*self.Width, (spec[0]+1)*self.Width, (spec[1]+1)*self.Width, fill=spec[2], width=1)
        for w in self.world_spec.walls:
            self.board.create_rectangle(w[0]*self.Width, w[1]*self.Width, (w[0]+1)*self.Width, (w[1]+1)*self.Width, fill="black", width=1)

    def try_move(self, dx, dy):
        if self.restart == True:
            self.restart_game()
        new_x = self.player[0] + dx
        new_y = self.player[1] + dy
        if (new_x >= 0) and (new_x < self.world_spec.x_width) and (new_y >= 0) and (new_y < self.world_spec.y_width) and not ((new_x, new_y) in self.world_spec.walls):
            self.board.coords(self.me, new_x*self.Width+self.Width*2/10, new_y*self.Width+self.Width*2/10, new_x*self.Width+self.Width*8/10, new_y*self.Width+self.Width*8/10)
            self.player = (new_x, new_y)
            self.set_cell_traversed(self.player)
        for spec in self.world_spec.specials:
            if new_x == spec[0] and new_y == spec[1]:
                self.restart = True
                return

    def call_up(self,event):
        self.try_move(0, -1)

    def call_down(self,event):
        self.try_move(0, 1)

    def call_left(self,event):
        self.try_move(-1, 0)

    def call_right(self,event):
        self.try_move(1, 0)

    def restart_game(self):
        self.player = (self.world_spec.x_player_start, self.world_spec.y_player_start)
        self.restart = False
        self.board.coords(self.me, self.player[0]*self.Width+self.Width*2/10, self.player[1]*self.Width+self.Width*2/10, self.player[0]*self.Width+self.Width*8/10, self.player[1]*self.Width+self.Width*8/10)

    def has_restarted(self):
        return self.restart

    def start_game(self):
        self.tk.mainloop()

