#!/usr/bin/env python

from costmap import Costmap2D
from obstacle import Obstacle

class BrushfireExpansion(object):
    """This class represents a brushfire style expansion algorithm"""
    def __init__(self, costmap):
        self.costmap = costmap
        
        self.ignition_cells = []
        self.wave_front = []
        
        self.first_step = True
    
    def set_ignition_cells(self, ignition_cells):
        """Sets the ignition cells, these are where the expansion should start from"""
        if type(ignition_cells) != list: 
            self.ignition_cells = [ignition_cells]
        else:
            self.ignition_cells = ignition_cells
    
    def step_solution(self):
        """This steps the solution, returns True if more work is required, otherwise False"""
        if self.first_step:
            self.first_step = False
            for cell in self.ignition_cells:
                self.costmap[cell[0], cell[1]] = 1
                self.wave_front.append(cell)
            return True
        new_wave_front = []
        for cell in self.wave_front:
            neighbors = self.costmap.get_neighbors(cell[0], cell[1])
            for neighbor in neighbors:
                if self.costmap[neighbor[0],neighbor[1]] == 0.0:
                    self.costmap[neighbor[0],neighbor[1]] = self.costmap[cell[0], cell[1]] + 1
                    new_wave_front.append(neighbor)
        if len(new_wave_front) == 0:
            return False
        self.wave_front = new_wave_front
        return True
    
    def solve(self):
        """Solves the expansion completely"""
        while self.step_solution():
            pass

if __name__ == '__main__':
    c = Costmap2D(10,20, resolution=0.5)
    Obstacle(3,3,3,3).draw(c)
    Obstacle(5,9,3,3).draw(c)
    Obstacle(4,16,3,3).draw(c)
    be = BrushfireExpansion(c)
    be.set_ignition_cells([(0,0)])
    be.solve()
    try:
        from matplotlib.pylab import imshow, show
        imshow(c.data.T, interpolation='nearest')
        show()
    except ImportError:
        import sys
        sys.stderr.write("You don't seem to have matplotlib, http://matplotlib.sourceforge.net/\n")
        print c
