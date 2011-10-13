#!/usr/bin/env python

import numpy as np

class Costmap2D(object):
    """
    This class represents an abitrary 2D costmap
    
    The width and height of the costmap in arbitrary units
    The dtype must match an option for dtype on a numpy array, default is 'int16'
    The resolution parameter can be thought of as the ration of units to cells.
      For example, with a costmap of 10x20 units and a resolution of 0.5, the actual
      grid would consist of 20x40 cells"""
    def __init__(self, width = 1, height = 1, dtype = 'int16', resolution = 1.0):
        self.width = int(width / float(resolution))
        self.height = int(height / float(resolution))
        self.resolution = resolution
        if self.width <= 0 or self.height <= 0:
            raise ValueError("Invalid width or height ({}x{}), less than or equal to zero."\
                                .format(self.width,self.height))
        self.dtype = dtype
        self.data = np.zeros(self.width*self.height, dtype = dtype)
        self.data = self.data.reshape(self.width, self.height)
        
        self.neighbors = np.zeros(8, dtype=self.dtype)
        self.on_update = None
    
    def __repr__(self):
        return self.__str__()
    
    def __str__(self):
        # I transpose this to print out correctly
        # order should be (col,row)/(x,y)/(e,n)/(l-r,u-d)
        # but it is printed (row,col)/...
        return self.data.T.__str__()
    
    def __getitem__(self, val):
        return self.data[val]
    
    def __setitem__(self, key, val):
        self.data[key] = val
        if self.on_update != None:
            self.on_update(key, val)
    
    def get_cell_values(self, cell_coordinates, return_numpy=True):
        """Returns a list of costmap cell values given a list of coordinates"""
        if type(cell_coordinates) in [list, set] and len(cell_coordinates) > 0:
            if return_numpy:
                cell_values = np.zeros(len(cell_coordinates), dtype=self.dtype)
                count = 0
            else:
                cell_values = []
            for cell_coord in cell_coordinates:
                x,y = cell_coord
                cell_value = self.data[x,y]
                if return_numpy:
                    cell_values[count] = cell_value
                    count += 1
                else:
                    cell_values.append(cell_value)
        else:
            print cell_coordinates
        return cell_values
    
    def get_neighbors(self, x, y):
        """Returns the 8 directional neighbors of the cell at the given x, y"""
        neighbors = []
        for y_ in [y-1, y, y+1]:
            if y_ < 0 or y_ > self.height-1: # If Y coordinate is invalid
                continue
            for x_ in [x-1, x, x+1]:
                if x_ == x and y_ == y: # If center
                    continue
                if x_ < 0 or x_ > self.width-1: # If X coordinate is invalid
                    continue
                neighbors.append((x_,y_))
        return neighbors
    
    def get_cardinals(self, x, y):
        """Returns the N, S, E, W neighbors of the cell at the given x, y"""
        neighbors = []
        for x_, y_ in [(x+1, y), (x, y+1), (x-1, y), (x,y-1)]:
            if 0 <= x_ < self.width and 0 <= y_ < self.height:
                neighbors.append((x_, y_))
        return neighbors
    

if __name__ == '__main__':
    c = Costmap2D(10, 20)
    print c[1,1]
    c[1,1] = -1
    print c[1,1]
    c[1,1:5] = np.array([1,2,3,4])
    print c.get_cell_values([(1,1),(1,2),(1,3),(1,4)])
    print type(c.get_cell_values([(1,1),(1,2),(1,3),(1,4)]))
    print c.get_cell_values([(1,1),(1,2),(1,3),(1,4)], return_numpy=False)
    print type(c.get_cell_values([(1,1),(1,2),(1,3),(1,4)], return_numpy=False))
    print c
    print c.get_neighbors(0,0)
    print c.get_neighbors(5,5)
    print c.get_neighbors(9,19)
    print set(c.get_cardinals(0,0)) == set([(0, 1), (1, 0)])
    print set(c.get_cardinals(5,5)) == set([(6, 5), (5, 6), (4, 5), (5, 4)])
    print set(c.get_cardinals(9,19)) == set([(8, 19), (9, 18)])
