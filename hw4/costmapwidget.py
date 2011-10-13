#!/usr/bin/env python

import sys
from Queue import Queue

from PySide import QtCore, QtGui

# Force PySide
import os; os.environ['QT_API'] = 'pyside'
from matplotlib.backends.backend_qt4agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
from matplotlib.backends.backend_qt4agg import NavigationToolbar2QTAgg as NavigationToolbar
from matplotlib.patches import Circle, Rectangle
from matplotlib.pylab import imshow

from costmap import Costmap2D
from obstacle import Obstacle

class Costmap2DFigure(FigureCanvas):
    costmap_changed = QtCore.Signal()
    
    """Implements an imshow figure for showing the costmap2d"""
    def __init__(self, costmap, parent=None, width=5.0, height=4.0, dpi=100, interpolation='nearest',
                    show_start = True, show_goal = True, show_colorbar = True):
        self.costmap = costmap
        self.freeze = False
        self.interpolation = interpolation
        self.fig = Figure(figsize=(width, height), dpi=dpi)
        self.axes = self.fig.add_subplot(1,1,1)
        # We want the axes cleared every time plot() is called
        self.axes.hold(False)
        
        self.show_start = show_start
        self.start_coord = (-0.5, -0.5)
        self.start = Rectangle(self.start_coord, 1, 1, color='g')
        self.show_goal = show_goal
        self.goal_coord = (self.costmap.width-1.5, self.costmap.height-1.5)
        self.goal = Rectangle(self.goal_coord, 1, 1, color='k')
        self.show_colorbar = show_colorbar
        
        self.compute_initial_figure()
        
        FigureCanvas.__init__(self, self.fig)
        self.setParent(parent)
        
        self.mpl_connect('button_release_event', self.on_mouse_release)
        
        FigureCanvas.setSizePolicy(self,
                                   QtGui.QSizePolicy.Expanding,
                                   QtGui.QSizePolicy.Expanding)
        
        FigureCanvas.updateGeometry(self)
        
        self.on_mouse_click = self.default_on_mouse_click
        
        # Idle control
        self.idle = True
        
        # Make Qt Connections
        self.connect_stuff()
        
        # Override costmap on change
        self.costmap.on_update = self.costmap_update_callback
    
    def on_mouse_release(self, e):
        """Gets called when a mouse button is released"""
        if self.on_mouse_click != None:
            self.on_mouse_click(e)
    
    def default_on_mouse_click(self, e):
        """Default function for mouse clicking"""
        if e.xdata == None or e.ydata == None:
            return
        from math import floor
        coord = (floor(e.xdata+0.5)-0.5, floor(e.ydata+0.5)-0.5)
        if -0.5 > coord[0] < self.costmap.width-1.5 or \
           -0.5 > coord[1] < self.costmap.height-1.5:
            return
        if e.button == 1:
            self.start_coord = coord
            self.start = Rectangle(coord, 1, 1, color='g')
        elif e.button == 3:
            self.goal_coord = coord
            self.goal = Rectangle(coord, 1, 1, color='k')
        else:
            return
        self.on_map_update()
    
    def connect_stuff(self):
        """Make Qt connections"""
        self.costmap_changed.connect(self.on_map_update)
    
    def costmap_update_callback(self, key, val):
        """Callback to handle when the map is updated"""
        if self.idle:
            self.idle = False
            self.costmap_changed.emit()
    
    def compute_initial_figure(self):
        """Plot the imshow"""
        axes = self.axes.imshow(self.costmap.data.T, interpolation=self.interpolation)
        if self.show_colorbar: self.colorbar = self.fig.colorbar(axes)
        if self.show_start: self.axes.add_artist(self.start)
        if self.show_goal: self.axes.add_artist(self.goal)
    
    def on_map_update(self):
        """Slot to handle the costmap_changed signal"""
        if self.freeze: return
        axes = self.axes.imshow(self.costmap.data.T, interpolation=self.interpolation)
        if self.show_colorbar:
            self.fig.delaxes(self.fig.axes[1])
            self.fig.subplots_adjust(right=0.90)
            self.colorbar = self.fig.colorbar(axes)
        if self.show_start: self.axes.add_artist(self.start)
        if self.show_goal: self.axes.add_artist(self.goal)
        self.draw()
        self.idle = True
    

class Costmap2DWidget(QtGui.QWidget):
    """Implements a widget that will display a costmap figure with a toolbar"""
    def __init__(self, costmap, parent = None, show_start = True, show_goal = True, 
                    show_colorbar = True):
        QtGui.QWidget.__init__(self, parent)
        self.costmap = costmap
        
        # Setup display
        self.canvas = Costmap2DFigure(costmap, show_start = show_start, show_goal = show_goal, 
                        show_colorbar = show_colorbar)
        self.toolbar = NavigationToolbar(self.canvas, self)
        
        # Setup layout
        layout = QtGui.QVBoxLayout()
        layout.addWidget(self.toolbar)
        layout.addWidget(self.canvas)
        self.setLayout(layout)
    

def _run_brushfire(c):
    """Runs the brushfire"""
    import time; time.sleep(3)
    from brushfire import BrushfireExpansion
    be = BrushfireExpansion(c)
    be.set_ignition_cells([(0,0)])
    while be.step_solution():
        pass
        # time.sleep(0.1)

def _run_voronoi_expansion(c):
    """Runs the voronoi expansion"""
    import time; time.sleep(3)
    from voronoi import VoronoiExpansion
    ve = VoronoiExpansion(c)
    while ve.step_solution():
        pass
        # time.sleep(0.1)

if __name__ == '__main__':
    try:
        c = Costmap2D(10,20,resolution=1.0)
        Obstacle(3,3,3,3).draw(c)
        Obstacle(5,9,3,3).draw(c)
        Obstacle(4,16,3,3).draw(c)
        
        app = QtGui.QApplication(sys.argv)
        cw = Costmap2DWidget(c)
        
        import threading
        threading.Thread(target=_run_brushfire, args=(c,)).start()
        # threading.Thread(target=_run_voronoi_expansion, args=(c,)).start()
        
        cw.show()
        sys.exit(app.exec_())
    except SystemExit:
        pass
    except:
        import traceback; traceback.print_exc()
