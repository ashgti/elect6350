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
    

def create_hw4_map():
    """Creates a field with obstacles as defined by the homework"""
    f = Field(10, 20)
    f.zero()
    f.add_obstacle(3,3,3,3)
    f.add_obstacle(5,9,3,3)
    f.add_obstacle(4,16,3,3)
    f.set_start(1,1)
    f.set_goal(10,20)
    return f

if __name__ == '__main__':
    try:
        f = create_hw4_map()
        print f
    except:
        import traceback; traceback.print_exc()
