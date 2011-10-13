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

    def __str__(self):
        return str((self.f_score[(self.x, self.y)], (self.x, self.y)))

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
            else:
                return cmp(dist_between((self.x, self.y), self.f.goal),
                           dist_between((other[0], other[1]), self.f.goal))
        else:
            other_pos = (other.x, other.y)
            tenative = cmp(self.f_score[my_pos], self.f_score[other_pos])
            return tenative
            # if tenative == 0:
            #     # If the two points have the same score, get the closest
            #     # to the goal.
            #     if self.x == other.x and \
            #             self.y == other.y:
            #         return 0
            #     else:
            #         return cmp(dist_between((self.x, self.y), self.f.goal),
            #                    dist_between((other.x, other.y), self.f.goal))
            # else:
            #     return tenative


def dist_between(point_a, point_b):
    """
    Pothagoreans theorm, the distance between 2 cells.
    This represents the cost to move from 1 cell to another.
    """
    a = point_b[0] - point_a[0]
    b = point_b[1] - point_a[1]
    result = math.sqrt(a ** 2.0 + b ** 2.0)
    # print result
    return result


def a_star(field, start, goal, heuristic_cost_estimate, neighbors_fn=None):
    """
    A function that returns a path as a list of coordinates.

    field = A representation of the playing field or graph.
    start = The starting position
    goal  = The target position
    heuristic_cost_estimate = A function to estimate the cost of moving into
                              a neighboring cell.
    neighbors_fn = None | A function to get neighbors of a point.

    return = A list of points that make up a path.
    """
    if neighbors_fn == None:
        neighbors_fn = field.get_neighbors

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

        if x == goal:
            print "Total Loops:", c
            path = reconstruct_path(came_from, came_from[goal])
            path.append(goal)
            print "Path Length:", len(path)
            print "Path Cost:", sum([f_score[x] for p in path])
            return path

        closedset.add(x)
        for y in neighbors_fn(*x):
            # If the value is in the closedset we don't need to revisit it
            if y in closedset:
                continue
            if field[y] == -1:
                continue
            tentative_g_score = g_score[x] + dist_between(x, y)

            if y not in openset:
                heapq.heappush(openset, Point(field, f_score, *y))
                tentative_is_better = True
            elif tentative_g_score < g_score[y]:
                tentative_is_better = True
            else:
                tentative_is_better = False

            if tentative_is_better:
                came_from[y] = x
                g_score[y] = tentative_g_score
                h_score[y] = heuristic_cost_estimate(field, y, goal)
                f_score[y] = g_score[y] + h_score[y]
                field[y] = f_score[y]
    return []


# 3 distinct heuristics
# I include the field incase future heuristics need to access values from it.
def crow(f, cell0, cell1):
    "A hypotense of a triangle."
    return dist_between(cell0, cell1)


def manhattan(f, cell0, cell1):
    """
    Calculate the manhattan distance.
    """
    return (abs(cell1[0] - cell0[0]) + abs(cell1[1] - cell0[1])) * 20


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

    c = Costmap2D(20, 20, resolution=0.5)
    c.goal = (c.width - 1, 0)
    c.start = (0, c.height - 1)
    Obstacle(2, 2, 1, 4).draw(c)
    Obstacle(2, 2, 8, 1).draw(c)
    Obstacle(16, 3, 1, 11).draw(c)
    Obstacle(6, 14, 11, 1).draw(c)

    d = copy.copy(c)
    d.data = c.data.copy()
    e = copy.copy(c)
    e.data = c.data.copy()
    cc = copy.copy(c)
    cc.data = c.data.copy()
    dc = copy.copy(c)
    dc.data = c.data.copy()
    ec = copy.copy(c)
    ec.data = c.data.copy()

    start = time.time()
    naive_r = a_star(c, c.start, c.goal, naive)
    end = time.time()

    print 'Naive:', end - start

    start = time.time()
    manhattan_r = a_star(d, d.start, d.goal, manhattan)
    end = time.time()

    print 'Manhattan:', end - start

    start = time.time()
    crow_r = a_star(e, e.start, e.goal, crow)
    end = time.time()

    print 'Crow:', end - start

    cc.start = (0, 0)
    cc.goal = (cc.width - 1, cc.height - 1)
    start = time.time()
    c_naive_r = a_star(cc, cc.start, cc.goal, naive)
    end = time.time()

    print 'Naive:', end - start

    dc.start = (0, 0)
    dc.goal = (dc.width - 1, dc.height - 1)
    start = time.time()
    c_manhattan_r = a_star(dc, dc.start, dc.goal, manhattan)
    end = time.time()

    print 'Manhattan:', end - start

    ec.start = (0, 0)
    ec.goal = (ec.width - 1, ec.height - 1)
    start = time.time()
    c_crow_r = a_star(ec, ec.start, ec.goal, crow)
    end = time.time()

    print 'Crow:', end - start

    # Sets the blocks of obstacles to a relatively distinct color
    naive_max_cell = c.data.max() * -1.0
    c.data[c.data == -1] = naive_max_cell / 2.0
    
    manhattan_max_cell = d.data.max() * -1.0
    d.data[d.data == -1] = manhattan_max_cell / 2.0
    
    crow_max_cell = e.data.max() * -1.0
    e.data[e.data == -1] = crow_max_cell / 2.0

    c_naive_max_cell = cc.data.max() * -1.0
    cc.data[cc.data == -1] = c_naive_max_cell / 2.0

    c_manhattan_max_cell = dc.data.max() * -1.0
    dc.data[dc.data == -1] = c_manhattan_max_cell / 2.0

    c_crow_max_cell = ec.data.max() * -1.0
    ec.data[ec.data == -1] = c_crow_max_cell / 2.0

    # Sets the line for the path to a very distinct color
    # max_counter makes the line change colors as it reaches the goal
    max_counter = 0
    for (x, y) in naive_r:
        max_counter += 1
        c.data[x, y] = naive_max_cell - max_counter
    
    max_counter = 0
    for (x, y) in manhattan_r:
        max_counter += 1
        d.data[x, y] = manhattan_max_cell - max_counter
    
    max_counter = 0
    for (x, y) in crow_r:
        max_counter += 1
        e.data[x, y] = crow_max_cell - max_counter

    max_counter = 0
    for (x, y) in c_naive_r:
        max_counter += 1
        cc.data[x, y] = c_naive_max_cell - max_counter

    max_counter = 0
    for (x, y) in c_manhattan_r:
        max_counter += 1
        dc.data[x, y] = c_manhattan_max_cell - max_counter

    max_counter = 0
    for (x, y) in c_crow_r:
        max_counter += 1
        ec.data[x, y] = c_crow_max_cell - max_counter

    fig = figure()
    fig.subplots_adjust(hspace=0.21, wspace=0.21,
                        bottom=0.07, top=0.96,
                        left=0.09, right=0.96)
    axes = fig.add_subplot(2, 3, 1)
    axes.imshow(c.data.T, interpolation='nearest')
    axes.set_title('Naive')
    axes = fig.add_subplot(2, 3, 2)
    axes.imshow(d.data.T, interpolation='nearest')
    axes.set_title('Manhattan')
    axes = fig.add_subplot(2, 3, 3)
    axes.imshow(e.data.T, interpolation='nearest')
    axes.set_title('Crow')
    axes = fig.add_subplot(2, 3, 4)
    axes.imshow(cc.data.T, interpolation='nearest')
    axes.set_title('Naive')
    axes = fig.add_subplot(2, 3, 5)
    axes.imshow(dc.data.T, interpolation='nearest')
    axes.set_title('Manhattan')
    axes = fig.add_subplot(2, 3, 6)
    axes.imshow(ec.data.T, interpolation='nearest')
    axes.set_title('Crow')
    show()
