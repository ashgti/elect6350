#!/usr/bin/env python

import sys

from costmap import Costmap2D
from obstacle import Obstacle

class PotentialField(object):
    """This class represents a Potential Field algorithm"""
    def __init__(self, costmap, start = (0,0), goal = None):
        self.costmap = costmap
        self.start = start
        if goal == None:
            self.goal = (self.costmap.width-1, self.costmap.height-1)
        
        self.katt = 1.0
        self.krep = 1.0
        self.roi = 10.0 # Region of Influence
        self.obstacle_cells = []
        
        self.first_run = True
    
    def prepare_field(self):
        """Prepares the potential field"""
        gx, gy = self.goal
        for (x, row) in enumerate(self.costmap.data):
            for (y, cell) in enumerate(row):
                if cell == -1.0: # If obstacle
                    self.obstacle_cells.append((x,y))
                else:
                    self.costmap.data[x,y] = self.distance(x,y,gx,gy)
    
    def distance(self, x, y, x_, y_):
        """Returns the potential at the given point"""
        return (x - x_)**2 + (y - y_)**2
    
    def step_solution(self):
        """This steps the solution, returns True if more work is required, otherwise False"""
        if self.first_run:
            self.first_run = False
            self.prepare_field()
            return True
        if self.obstacle_cells == []:
            return False
        obx, oby = self.obstacle_cells.pop()
        for (x, row) in enumerate(self.costmap.data):
            for (y, cell) in enumerate(row):
                if cell == -1.0: # If obstacle
                    continue
                replusion = self.distance(x,y,obx,oby)
                if replusion <= self.roi:
                    self.costmap[x,y] += replusion
        return True
    
    def solve(self):
        """Solves the expansion completely"""
        while self.step_solution():
            pass
    

if __name__ == '__main__':
    c = Costmap2D(10,20, resolution=0.25)
    Obstacle(3,3,3,3).draw(c)
    Obstacle(5,9,3,3).draw(c)
    Obstacle(4,16,3,3).draw(c)
    pf = PotentialField(c)
    from matplotlib.pylab import imshow, show
    imshow(c.data.T, interpolation='nearest')
    show()
    pf.solve()
    try:
        from matplotlib.pylab import imshow, show
        imshow(c.data.T, interpolation='nearest')
        show()
    except ImportError:
        import sys
        sys.stderr.write("You don't seem to have matplotlib, http://matplotlib.sourceforge.net/\n")
        print c
