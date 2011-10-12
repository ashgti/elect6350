#!/usr/bin/env python

from brushfire import BrushfireExpansion

from costmap import Costmap2D
from obstacle import Obstacle

class VoronoiExpansion(BrushfireExpansion):
    """This class represents a Voronoi algorithm using a brushfire style expansion"""
    def __init__(self, costmap):
        BrushfireExpansion.__init__(self, costmap)
        self.set_ignition_cells(self.get_boundry_cells())
    
    def get_boundry_cells(self):
        """This gets the cells around the perimeter of the map and from around the obstacles"""
        boundry_cells = []
        for (x, row) in enumerate(self.costmap):
            for (y, cell) in enumerate(row):
                # If cell has been set (!=0) don't process
                if cell == 0.0:
                    # If it is on the edge of the map or If it touches an non-traversable
                    if self.on_edge(x,y) or \
                     -1.0 in self.costmap.get_cell_values(self.costmap.get_neighbors(x,y)):
                        boundry_cells.append((x,y))
        return boundry_cells
    
    def on_edge(self, x, y):
        """Returns True if the cell at x,y is on the edge of the map, otherwise False"""
        if x % self.costmap.width in [0, self.costmap.width-1]:
            return True
        if y % self.costmap.height in [0, self.costmap.height-1]:
            return True
        return False
    
    def solve(self):
        """Solves the voronoi algorithm"""
        BrushfireExpansion.solve(self)
        # Now extract the voronoi lines
        # TODO: extract the voronoi lines
    

if __name__ == '__main__':
    c = Costmap2D(10,20, resolution=0.5)
    Obstacle(3,3,3,3).draw(c)
    Obstacle(5,9,3,3).draw(c)
    Obstacle(4,16,3,3).draw(c)
    ve = VoronoiExpansion(c)
    ve.solve()
    try:
        from matplotlib.pylab import imshow, show
        imshow(c.data.T, interpolation='nearest')
        show()
    except ImportError:
        import sys
        sys.stderr.write("You don't seem to have matplotlib, http://matplotlib.sourceforge.net/\n")
        print c
