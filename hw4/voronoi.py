from field import Field, create_hw4_map

class Voronoi(object):
    """Implementation of Voronoi"""
    def __init__(self, field):
        self.field = field
        
        self.border_cells = []
        self.get_initial_border_cells()
        
        self.first_step = True
    
    def get_initial_border_cells(self):
        """This returns the initial border cells"""
        for (y, row) in enumerate(self.field):
            for (x, cell) in enumerate(row):
                # If cell has been set (!=0) don't process
                if cell == 0.0:
                    # If it is on the edge of the map or If it touches an non-traversable
                    if self.on_edge(x,y) or -1.0 in self.neighbor_cells(x,y):
                        self.border_cells.append((x,y))
                        # self.field[y,x] = 1
        return self.border_cells
    
    def on_edge(self, x, y):
        """returns true if the cell is on the edge of the map"""
        temp = self.field[y, x] # If this fails the coordinates are invalid on this field
        if x % self.field.width in [0, self.field.width-1]:
            return True
        if y % self.field.height in [0, self.field.height-1]:
            return True
        return False
    
    def neighbors(self, x, y):
        """Returns the neighbors of the given coordinate"""
        temp = self.field[y, x] # If this fails the coordinates are invalid on this field
        neighbors = []
        possible_neighbors = [(x-1,y+1), (x,y+1), (x+1,y+1),
                              (x-1,y),            (x+1,y),
                              (x-1,y-1), (x,y-1), (x+1,y-1)]
        for pn in possible_neighbors:
            if pn[0] >= self.field.width or pn[0] < 0:
                continue
            if pn[1] >= self.field.height or pn[1] < 0:
                continue
            neighbors.append(pn)
        
        return neighbors
    
    def neighbor_cells(self,x,y):
        """returns the neighboring cells"""
        neighbors = self.neighbors(x,y)
        return self.field.get_cells_from_coordinates(neighbors)
    
    def step_solution(self):
        """Steps the expansion of the voronoi solution"""
        if self.first_step:
            self.first_step = False
            self.field.fill_cells(self.border_cells, 1)
            return
        new_borders = []
        for cell in self.border_cells:
            cell_value = self.field[cell[1], cell[0]]
            for neighbor in self.neighbors(cell[0], cell[1]):
                if self.field[neighbor[1], neighbor[0]] == 0.0 and neighbor not in self.border_cells:
                    self.field[neighbor[1], neighbor[0]] = cell_value+1
                    new_borders.append((neighbor[0], neighbor[1]))
        self.border_cells = new_borders
    
    def solve(self):
        """Solves for the Voronoi diagram"""
        # Loop until the costmap has been expanded
        while len(self.border_cells) > 0:
            self.step_solution()
        
    

def plot_performance():
    """Calculates the run time for many map scales and plots the times vs the scales"""
    scales = [1+0.25*x for x in range(30)]
    times = []
    for scale in scales:
        f = create_hw4_map(scale)
        
        f[0,0] = -1
        
        v = Voronoi(f)
        v.border_cells = v.neighbors(0,0)
        
        import time
        start = time.time()
        
        v.solve()
        
        t = time.time() - start
        times.append(t)
        print "Processing a field of size {}x{} took".format(f.width, f.height), t, "seconds"
        print f
    print times
    from matplotlib.pyplot import plot, show
    plot(scales, times)
    show()

def run_hw4_voronoi():
    """Runs the voronoi on the hw4 map"""
    f = create_hw4_map(1)
    
    f[0,0] = -1
    
    v = Voronoi(f)
    v.border_cells = v.neighbors(0,0)
    v.solve()
    
    print f

if __name__ == '__main__':
    try:
        plot_performance()
        # run_hw4_voronoi()
    except:
        import traceback; traceback.print_exc()
