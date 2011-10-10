#!/usr/bin/env python

import numpy as np
from obstacle import Obstacle

class Field(np.ndarray):
    """Represents a theoretical field for a robot with obstacles in it."""
    def __new__(cls, width, height, dtype = "int32", buffer=None, offset=0,
                strides=None, order=None):
        obj = np.ndarray.__new__(cls, (height, width), dtype, buffer, offset, strides, order)
        obj.width = width
        obj.height = height
        obj.obstacles = []
        return obj
    
    def __init__(self, width, height, dtype = "int32"):
        self._dtype = dtype
        self.width = width
        self.height = height
        
        self.start = (-1,-1)
        self.goal = (-1,-1)
        
        self.draw_obstacles()
        
        self.obstacles = []
    
    def add_obstacle(self, origin_x, origin_y, width, height):
        """Add an obstacles to the map"""
        self.obstacles.append(Obstacle(origin_x-1, origin_y-1, width, height))
        
        self.draw_obstacles()
    
    def set_start(self, x, y):
        """Sets the starting point"""
        self.start = (x-1,y-1)
    
    def set_goal(self, x, y):
        """Sets the goal point"""
        self.goal = (x-1,y-1)
    
    def zero(self):
        """Resets the grid to zero"""
        self[:] = 0.0
    
    def draw_obstacles(self):
        """Draw the obstacles on the map"""
        if self.obstacles == []: return
        for obstacle in self.obstacles:
            origin = obstacle.origin
            size = obstacle.size
            self[origin[1]:origin[1]+size[1],origin[0]:origin[0]+size[0]] = -1.0
    
    def get_cells_from_coordinates(self, coords):
        """Returns a list of cell values given a set of cell coordinates"""
        cell_values = []
        for cell_coord in coords:
            cell_values.append(self[cell_coord[1], cell_coord[0]])
        return cell_values
    

def create_hw4_map(scale = 1):
    """Creates a field with obstacles as defined by the homework"""
    f = Field(int(10*scale), int(20*scale))
    f.zero()
    f.add_obstacle(int(3*scale),int(3*scale),int(3*scale),int(3*scale))
    f.add_obstacle(int(5*scale),int(9*scale),int(3*scale),int(3*scale))
    f.add_obstacle(int(4*scale),int(16*scale),int(3*scale),int(3*scale))
    f.set_start(1,1)
    f.set_goal(int(10*scale),int(20*scale))
    return f

if __name__ == '__main__':
    try:
        f = create_hw4_map()
        print f
    except:
        import traceback; traceback.print_exc()
