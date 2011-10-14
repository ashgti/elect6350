#!/usr/bin/env python

import sys
from math import floor

from threading import Lock

from PySide import QtCore, QtGui

from costmap import Costmap2D
from costmapwidget import Costmap2DWidget
from obstacle import Obstacle
from brushfire import BrushfireExpansion
from potentialfield import PotentialField
from voronoi import VoronoiExpansion
from algorithmwidget import AlgorithmWidget
from a_star import AStar, manhattan, naive, crow

DEFAULT_WIDTH = 20
DEFAULT_HEIGHT = 10
DEFAULT_RESOLUTION = 0.25

DEFAULT_TIMEOUT = 0.1

class PotentialAlgorithmWidget(AlgorithmWidget):
    def __init__(self, parent=None, colorbar = False):
        self.colorbar = colorbar
        AlgorithmWidget.__init__(self, "Potential Field Algorithm", parent)
        self.pack_buttons()
    
    def setup_algorithm(self):
        """Sets up the algorithm"""
        self.costmap = Costmap2D(DEFAULT_WIDTH, DEFAULT_HEIGHT, resolution=DEFAULT_RESOLUTION)
        Obstacle(3,3,3,3).draw(self.costmap)
        Obstacle(9,5,3,3).draw(self.costmap)
        Obstacle(16,4,3,3).draw(self.costmap)
        
        self.costmap_widget = Costmap2DWidget(self.costmap, parent = self, show_goal = False,
                                                show_start = False, show_colorbar = self.colorbar)
        self.pf = PotentialField(self.costmap)
    
    def step_solution(self):
        return self.pf.step_solution()
    
    def reset_algorithm(self):
        self.costmap[:] = 0.0
        Obstacle(3,3,3,3).draw(self.costmap)
        Obstacle(9,5,3,3).draw(self.costmap)
        Obstacle(16,4,3,3).draw(self.costmap)
        
        self.pf = PotentialField(self.costmap)
        self.costmap_widget.canvas.on_map_update()
    

class AStarAlgorithmWidget(AlgorithmWidget):
    def __init__(self, parent=None):
        self.heuristic = naive
        AlgorithmWidget.__init__(self, "A* Algorithm", parent)
        self.combo_box = QtGui.QComboBox(parent)
        self.combo_box.addItems(["naive", 'manhattan', 'crow'])
        self.combo_box.currentIndexChanged.connect(self.select_heuristic)
        self.buttons.append(self.combo_box)
        self.pack_buttons()

    def select_heuristic(self, index):
        if index == 0:
            self.heuristic = naive
        elif index == 1:
            self.heuristic = manhattan
        elif index == 2:
            self.heuristic = crow
        self.a_star.heuristic_cost_estimate = self.heuristic

    def setup_algorithm(self):
        """Sets up the algorithm"""
        self.costmap = Costmap2D(DEFAULT_WIDTH, DEFAULT_HEIGHT,
                                 resolution=DEFAULT_RESOLUTION)
        Obstacle(3,3,3,3).draw(self.costmap)
        Obstacle(9,5,3,3).draw(self.costmap)
        Obstacle(16,4,3,3).draw(self.costmap)

        self.costmap_widget = Costmap2DWidget(self.costmap,
                                              parent=self, 
                                              show_goal=False,
                                              show_colorbar=True)
        self.costmap_widget.canvas.show_start = True
        self.costmap_widget.canvas.show_goal = True
        temp = self.costmap_widget.canvas.start_coord
        self.start_coord = (floor(temp[0]+0.5), floor(temp[1]+0.5))
        temp = self.costmap_widget.canvas.goal_coord
        self.goal_coord = (floor(temp[0]+0.5), floor(temp[1]+0.5))
        self.a_star = AStar(self.costmap,
                            self.start_coord,
                            self.goal_coord,
                            self.heuristic)

    def step_solution(self):
        """Steps the solution"""
        # self.costmap_widget.canvas.freeze = True
        # count = 0
        # while count < 25:
        #     count += 1
        #     result = self.a_star.step_solution()
        #     if result == False:
        #         self.costmap_widget.canvas.freeze = False
        #         self.costmap_widget.canvas.on_map_update()
        #         return result
        # self.costmap_widget.canvas.freeze = False
        # self.costmap_widget.canvas.on_map_update()
        # return True
        return self.a_star.step_solution()

    def reset_algorithm(self):
        """Resets the algorithm"""
        self.costmap_widget.canvas.freeze = True
        self.costmap[:] = 0.0
        Obstacle(3,3,3,3).draw(self.costmap)
        Obstacle(9,5,3,3).draw(self.costmap)
        Obstacle(16,4,3,3).draw(self.costmap)

        temp = self.costmap_widget.canvas.start_coord
        self.start_coord = (floor(temp[0]+0.5), floor(temp[1]+0.5))
        temp = self.costmap_widget.canvas.goal_coord
        self.goal_coord = (floor(temp[0]+0.5), floor(temp[1]+0.5))
        self.a_star = AStar(self.costmap,
                            self.start_coord,
                            self.goal_coord,
                            self.heuristic)
        self.costmap_widget.canvas.freeze = False
        self.costmap_widget.canvas.on_map_update()


class BrushfireAlgorithmWidget(AlgorithmWidget):
    def __init__(self, parent = None, colorbar = False):
        self.colorbar = colorbar
        AlgorithmWidget.__init__(self, "Brushfire Algorithm", parent)
        self.pack_buttons()
    
    def setup_algorithm(self):
        """Sets up the algorithm"""
        self.costmap = Costmap2D(DEFAULT_WIDTH, DEFAULT_HEIGHT, resolution=DEFAULT_RESOLUTION)
        Obstacle(3,3,3,3).draw(self.costmap)
        Obstacle(9,5,3,3).draw(self.costmap)
        Obstacle(16,4,3,3).draw(self.costmap)
        
        self.costmap_widget = Costmap2DWidget(self.costmap, parent = self, show_goal = False,
                                                show_colorbar = self.colorbar)
        self.costmap_widget.canvas.show_start = True
        self.costmap_widget.canvas.show_goal = False
        self.be = BrushfireExpansion(self.costmap)
        temp = self.costmap_widget.canvas.start_coord
        self.start_coord = (floor(temp[0]+0.5), floor(temp[1]+0.5))
        self.be.set_ignition_cells([self.start_coord])
    
    def step_solution(self):
        """Steps the solution"""
        return self.be.step_solution()
    
    def reset_algorithm(self):
        """Resets the algorithm"""
        self.costmap_widget.canvas.freeze = True
        self.costmap[:] = 0.0
        Obstacle(3,3,3,3).draw(self.costmap)
        Obstacle(9,5,3,3).draw(self.costmap)
        Obstacle(16,4,3,3).draw(self.costmap)
        
        self.be = BrushfireExpansion(self.costmap)
        temp = self.costmap_widget.canvas.start_coord
        self.start_coord = (floor(temp[0]+0.5), floor(temp[1]+0.5))
        self.be.set_ignition_cells([self.start_coord])
        self.costmap_widget.canvas.freeze = False
        self.costmap_widget.canvas.on_map_update()
    

class VoronoiAlgorithmWidget(AlgorithmWidget):
    def __init__(self, parent = None, colorbar = False):
        self.colorbar = colorbar
        AlgorithmWidget.__init__(self, "Voronoi Algorithm", parent)
        self.pack_buttons()

    def setup_algorithm(self):
        """Sets up the algorithm"""
        self.costmap = Costmap2D(DEFAULT_WIDTH, DEFAULT_HEIGHT, resolution=DEFAULT_RESOLUTION)
        Obstacle(3,3,3,3).draw(self.costmap)
        Obstacle(9,5,3,3).draw(self.costmap)
        Obstacle(16,4,3,3).draw(self.costmap)

        self.costmap_widget = Costmap2DWidget(self.costmap, parent = self, show_goal = False,
                                                show_colorbar = self.colorbar)
        self.costmap_widget.canvas.show_start = False
        self.costmap_widget.canvas.show_goal = False
        self.vo = VoronoiExpansion(self.costmap)

    def step_solution(self):
        """Steps the solution"""
        result = self.vo.step_solution()
        self.costmap_widget.canvas.on_map_update()

        return result

    def reset_algorithm(self):
        """Resets the algorithm"""
        self.costmap_widget.canvas.freeze = True
        self.costmap[:] = 0.0
        Obstacle(3,3,3,3).draw(self.costmap)
        Obstacle(9,5,3,3).draw(self.costmap)
        Obstacle(16,4,3,3).draw(self.costmap)

        self.vo = VoronoiExpansion(self.costmap)
        self.costmap_widget.canvas.freeze = False
        self.costmap_widget.canvas.on_map_update()


class Homework4App(QtGui.QWidget):
    def __init__(self, parent=None):
        QtGui.QWidget.__init__(self, parent)
        
        ba = BrushfireAlgorithmWidget(self, True)
        pa = PotentialAlgorithmWidget(self, True)
        aa = AStarAlgorithmWidget(self)
        va = VoronoiAlgorithmWidget(self, True)
        
        layout = QtGui.QHBoxLayout()
        l1 = QtGui.QVBoxLayout()
        l1.addWidget(ba)
        l1.addWidget(pa)
        l2 = QtGui.QVBoxLayout()
        l2.addWidget(aa)
        l2.addWidget(va)
        layout.addLayout(l1)
        layout.addLayout(l2)
        # layout.addWidget(va)
        self.setLayout(layout)
    

if __name__ == '__main__':
    app = QtGui.QApplication(sys.argv)
    hw4app = Homework4App()
    hw4app.show()
    sys.exit(app.exec_())
