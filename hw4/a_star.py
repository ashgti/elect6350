import math
import numpy as np
import heapq
from sys import maxint
import collections


class Point(object):
    """
    A point represents a position on the map. However, they are sorted by their
    distance to the goal.
    """
    def __init__(self, f, x, y):
        """
        Creates a new Point, it takes the field, and an f_score array as well.
        """
        self.f = f
        self.x = x
        self.y = y

    def __cmp__(self, other):
        """
        Compares a Point to another point or a tuple (x, y).
        """
        if type(other) == tuple:
            if self.x == other[0] and self.y == other[1]:
                return 0
            if dist_between((other[0], other[1]), self.f.goal)\
               > dist_between((self.x, self.y), self.f.goal):
                return -1
            else:
                return 1
        else:
            if self.x == other.x and self.y == other.y:
                return 0
            if dist_between((other.x, other.y), self.f.goal)\
               > dist_between((self.x, self.y), self.f.goal):
                return -1
            else:
                return 1


def dist_between(point_a, point_b):
    """
    Pothagoreans theorm, the distance between 2 cells.
    This represents the cost to move from 1 cell to another.
    """
    a = point_b[0] - point_a[0]
    b = point_b[1] - point_a[1]
    return math.sqrt(a ** 2 + b ** 2)


def a_star(field, start, goal, heuristic_cost_estimate):
    "A function that returns a path as a list of coordinates"
    width = field.width
    height = field.height

    g_score = np.zeros(width * height, dtype='int32').reshape(width, height)
    h_score = np.zeros(width * height, dtype='int32').reshape(width, height)
    f_score = np.zeros(width * height, dtype='int32').reshape(width, height)

    # The set of nodes already evaluated.
    closedset = set()

    # The set of tentative nodes to be evaluated, initially containing the
    # start node
    openset = [Point(field, *start)]
    heapq.heapify(openset)

    # The map of navigated nodes.
    came_from = {start: None}

    # Cost from start along best known path.
    g_score[start] = 0
    h_score[start] = heuristic_cost_estimate(field, start, goal)

    # Estimated total cost from start to goal through y.
    f_score[start] = g_score[start] + h_score[start]

    while openset:
        # Find the lowest scoring node in the openset
        current_node = heapq.heappop(openset)
        x = (current_node.x, current_node.y)

        if x == goal:
            path = reconstruct_path(came_from, came_from[goal])
            path.append(goal)
            return path

        closedset.add(x)
        for y in field.get_cardinals(*x):
            if y in closedset:
                continue
            if field[y] == -1:
                continue
            tentative_g_score = g_score[x] + dist_between(x, y)

            if y not in openset:
                heapq.heappush(openset, Point(field, *y))
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
                     (cell1[1] - cell0[1]) ** 2)


def manhattan(f, cell0, cell1):
    """
    Calculate the manhattan distance.
    """
    return (abs(cell1[0] - cell0[0]) + abs(cell1[1] - cell0[1]))


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
    from matplotlib.pylab import imshow, show
    import time

    c = Costmap2D(10, 20, resolution=0.2)
    c.goal = (c.width - 1, c.height - 1)
    c.start = (0, 0)
    Obstacle(3, 3, 3, 10).draw(c)
    Obstacle(5, 9, 3, 10).draw(c)
    Obstacle(4, 16, 3, 3).draw(c)

    start = time.time()
    r = a_star(c, c.start, c.goal, manhattan)
    end = time.time()

    max_cell = c.data.max() * -1
    # Sets the blocks of obstacles to a relatively distinct color
    c.data[c.data == -1] = max_cell / 2

    # Sets the line for the path to a very distinct color
    for (x, y) in r:
        c.data[x, y] = max_cell

    print str(end - start) + "s"
    imshow(c.data.T, interpolation='nearest')
    show()
