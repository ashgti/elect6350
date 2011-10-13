import math
import numpy as np
import heapq
import collections
import copy


class Point(object):
    """
    A point represents a position on the map. However, they are sorted by their
    distance to the goal.
    """
    def __init__(self, f, f_score, x, y):
        """
        Creates a new Point, it takes the field, and an f_score array as well.
        """
        self.f = f
        self.x = x
        self.y = y
        self.f_score = f_score

    def __cmp__(self, other):
        """
        Compares a Point to another point or a tuple (x, y).
        
        TODO(ash_gti): Check this. It seems off...
        """
        my_pos = (self.x, self.y)
        if type(other) == tuple:
            # Tuples are only passed to see if we are in the openset
            # thus, we don't really care about the f_score, we only
            # need to check for equality really.
            other_pos = other
            if self.x == other[0] and self.y == other[1]:
                return 0
            elif dist_between((other[0], other[1]), self.f.goal)\
               > dist_between((self.x, self.y), self.f.goal):
                return -1
            else:
                return 1
        else:
            other_pos = (other.x, other.y)
            # if self.x == other.x and \
            #         self.y == other.y:
            #     return 0
            # elif dist_between((other.x, other.y), self.f.goal)\
            #         > dist_between((self.x, self.y), self.f.goal):
            #     return -1
            # else:
            #     return 1
            return cmp(self.f_score[my_pos], self.f_score[other_pos])

def dist_between(point_a, point_b):
    """
    Pothagoreans theorm, the distance between 2 cells.
    This represents the cost to move from 1 cell to another.
    """
    a = point_b[0] - point_a[0]
    b = point_b[1] - point_a[1]
    result = math.sqrt(a ** 2 + b ** 2)
    # print result
    return result


def a_star(field, start, goal, heuristic_cost_estimate, diagonal=True):
    "A function that returns a path as a list of coordinates"
    width = field.width
    height = field.height

    g_score = np.zeros(width * height, dtype=float).reshape(width, height)
    h_score = np.zeros(width * height, dtype=float).reshape(width, height)
    f_score = np.zeros(width * height, dtype=float).reshape(width, height)

    # The set of nodes already evaluated.
    closedset = set()

    # The set of tentative nodes to be evaluated, initially containing the
    # start node
    openset = [Point(field, f_score, *start)]
    heapq.heapify(openset)

    # The map of navigated nodes.
    came_from = {start: None}

    # Cost from start along best known path.
    g_score[start] = 0
    h_score[start] = heuristic_cost_estimate(field, start, goal)

    # Estimated total cost from start to goal through y.
    f_score[start] = g_score[start] + h_score[start]

    c = 0

    while openset:
        c += 1
        # Find the lowest scoring node in the openset
        current_node = heapq.heappop(openset)
        x = (current_node.x, current_node.y)

        # if c > 200:
            # imshow(field.data.T, interpolation='nearest')
            # show()

        if x == goal:
            print c
            path = reconstruct_path(came_from, came_from[goal])
            path.append(goal)
            print len(path)
            return path

        closedset.add(x)
        if diagonal:
            neighbors = field.get_neighbors(*x)
        else:
            neighbors = field.get_cardinals(*x)
        for y in neighbors:
            if y in closedset:
                continue
            if field[y] == -1:
                continue
            tentative_g_score = g_score[x] + dist_between(x, y)

            if y not in openset:
                heapq.heappush(openset, Point(field, f_score, *y))
                tentative_is_better = True
            elif tentative_g_score > g_score[y]:
                tentative_is_better = True
            else:
                tentative_is_better = False

            if tentative_is_better:
                came_from[y] = x
                g_score[y] = tentative_g_score
                h_score[y] = heuristic_cost_estimate(field, y, goal)
                f_score[y] = g_score[y] + h_score[y]
                field[y] = f_score[y]
    return None


# 3 distinct heuristics
# I include the field incase future heuristics need to access values from it.
def crow(f, cell0, cell1):
    "A hypotense of a triangle."
    return math.sqrt((cell1[0] - cell0[0]) ** 2 + \
                     (cell1[1] - cell0[1]) ** 2) * 10


def manhattan(f, cell0, cell1):
    """
    Calculate the manhattan distance.
    """
    return (abs(cell1[0] - cell0[0]) + abs(cell1[1] - cell0[1])) * 10


def naive(f, cell0, cell1):
    "Simply returns 0"
    return 0


def reconstruct_path(came_from, current_node):
    """
    Takes a dictionary with the path in it and follows it to the root.
    """
    if came_from[current_node]:
        p = reconstruct_path(came_from, came_from[current_node])
        p.append(current_node)
        return p
    else:
        return [current_node]


if __name__ == '__main__':
    from costmap import Costmap2D
    from obstacle import Obstacle
    from matplotlib.pyplot import plot, show
    from matplotlib.pylab import imshow, show, figure
    import time

    c = Costmap2D(10, 20, resolution=0.2)
    c.goal = (c.width - 1, c.height - 1)
    c.start = (0, 0)
    Obstacle(3, 3, 2, 10).draw(c)
    Obstacle(5, 9, 3, 10).draw(c)
    Obstacle(0, 16, 6, 1).draw(c)
    Obstacle(6, 7, 4, 1).draw(c)
    
    d = copy.copy(c)
    d.data = c.data.copy()
    e = copy.copy(c)
    e.data = c.data.copy()

    start = time.time()
    naive_r = a_star(c, c.start, c.goal, naive, True)
    end = time.time()

    print 'Naive:', end - start

    start = time.time()
    manhattan_r = a_star(d, d.start, d.goal, manhattan, True)
    end = time.time()

    print 'Manhattan:', end - start

    start = time.time()
    crow_r = a_star(e, e.start, e.goal, crow, True)
    end = time.time()
    
    print 'Crow:', end - start

    # Sets the blocks of obstacles to a relatively distinct color
    naive_max_cell = c.data.max() * -1
    c.data[c.data == -1] = naive_max_cell / 2.0

    manhattan_max_cell = d.data.max() * -1
    d.data[d.data == -1] = manhattan_max_cell / 2.0

    crow_max_cell = e.data.max() * -1
    e.data[e.data == -1] = crow_max_cell / 2.0

    # Sets the line for the path to a very distinct color
    for (x, y) in naive_r:
        c.data[x, y] = naive_max_cell

    for (x, y) in manhattan_r:
        d.data[x, y] = manhattan_max_cell

    for (x, y) in crow_r:
        e.data[x, y] = crow_max_cell

    fig = figure()
    fig.subplots_adjust(hspace=0.01, wspace=0.01,
                        bottom=0.07, top=1.0,
                        left=0.04, right=1.0)
    axes = fig.add_subplot(1, 3, 1)
    axes.imshow(c.data.T, interpolation='nearest')
    axes.set_title('Naive')
    axes = fig.add_subplot(1, 3, 2)
    axes.imshow(d.data.T, interpolation='nearest')
    axes.set_title('Manhattan')
    axes = fig.add_subplot(1, 3, 3)
    axes.imshow(e.data.T, interpolation='nearest')
    axes.set_title('Crow')
    show()
