import math
import numpy as np
import heapq
import collections
import copy


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


class AStar(object):
    """
    AStar represents an instance of the A* algorithm.
    """
    def __init__(self, field, start, goal, heuristic_cost_estimate):
        """
        Creates a new AStar instance.
        """
        self.start = start
        self.goal = goal
        self.width = field.width
        self.height = field.height
        self.field = field

        self.heuristic_cost_estimate = heuristic_cost_estimate

        self.g_score = np.zeros(self.width * self.height, dtype=float)\
                         .reshape(self.width, self.height)
        self.h_score = np.zeros(self.width * self.height, dtype=float)\
                         .reshape(self.width, self.height)
        self.f_score = np.zeros(self.width * self.height, dtype=float)\
                         .reshape(self.width, self.height)

        # The set of nodes already evaluated.
        self.closedset = set()

        # The set of tentative nodes to be evaluated, initially containing the
        # start node
        self.openset = [(self.f_score[start], start)]
        heapq.heapify(self.openset)

        # The map of navigated nodes.
        self.came_from = {start: None}

        # The path to the goal
        self.path = []

        # Cost from start along best known path.
        self.g_score[start] = 0
        self.h_score[start] = self.heuristic_cost_estimate(field, start, goal)

        # Estimated total cost from start to goal through y.
        self.f_score[start] = self.g_score[start] + self.h_score[start]

    def solve(self):
        """
        Solves for the path.
        """
        while self.step_solution():
            pass
        self.draw_path()
        return True

    def draw_path(self):
        """
        Draws the path in the field.
        """
        max_cell = self.field.data.max() * -1.0
        max_counter = 0
        # self.field[self.field.data == -1] = max_cell / 2.0
        if self.path:
            for (x, y) in self.path:
                max_counter += 1
                self.field[x, y] = -20

    def step_solution(self):
        """
        A function that returns a path as a list of coordinates.

        field = A representation of the playing field or graph.
        start = The starting position
        goal  = The target position
        heuristic_cost_estimate = A function to estimate the cost of moving
                                  into a neighboring cell.
        neighbors_fn = None | A function to get neighbors of a point.

        return = A list of points that make up a path.
        """
        # Find the lowest scoring node in the openset
        try:
            current_node = heapq.heappop(self.openset)
        except IndexError:
            return False
        x = current_node[1]

        if x == self.goal:
            if x == self.goal and x == self.start:
                self.path = []
            else:
                self.path = reconstruct_path(self.came_from,
                                             self.came_from[self.goal])
            self.path.append(self.goal)
            self.draw_path()
            return False

        self.closedset.add(x)
        for y in self.field.get_neighbors(*x):
            # If the value is in the closedset we don't need to revisit it
            if y in self.closedset:
                continue
            if self.field[y] == -1:
                continue

            tentative_g_score = self.g_score[x] + dist_between(x, y)

            # Strip out the f_scores from the openset and check if it exists
            if y not in [v[1] for v in self.openset]:
                self.came_from[y] = x
                self.g_score[y] = tentative_g_score
                self.h_score[y] = self.heuristic_cost_estimate(self.field,
                                                               y,
                                                               self.goal)
                self.f_score[y] = self.g_score[y] + self.h_score[y]
                self.field[y] = self.f_score[y]
                heapq.heappush(self.openset, (self.f_score[y], y))
            elif tentative_g_score < self.g_score[y]:
                self.came_from[y] = x
                self.g_score[y] = tentative_g_score
                self.h_score[y] = self.heuristic_cost_estimate(self.field,
                                                               y,
                                                               self.goal)
                self.f_score[y] = self.g_score[y] + self.h_score[y]
                self.field[y] = self.f_score[y]
        return True


# 3 distinct heuristics
# I include the field incase future heuristics need to access values from it.
def crow(f, cell0, cell1):
    "A hypotense of a triangle."
    return dist_between(cell0, cell1)


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
    from matplotlib.pylab import imshow, show, figure
    import time

    c = Costmap2D(10, 20, resolution=0.5)
    c.goal = (0, 0)
    c.start = (c.width - 1, c.height - 1)
    Obstacle(4, 3, 3, 3).draw(c)
    Obstacle(5, 9, 3, 3).draw(c)
    Obstacle(4, 16, 3, 3).draw(c)

    a_star = AStar(c, c.start, c.goal, naive)

    start = time.time()
    a_star.solve()
    end = time.time()

    print 'Naive:', end - start

    imshow(a_star.field.data, interpolation='nearest')
    show()
