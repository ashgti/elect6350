#!/usr/bin/env python

import sys
from Queue import Queue

from PySide import QtCore, QtGui

import matplotlib
matplotlib.use('AGG')
from matplotlib.pylab import gcf, imshow, draw

from costmap import Costmap2D
from obstacle import Obstacle

class Costmap2DWidget(QtGui.QWidget):
    costmap_changed = QtCore.Signal()
    
    """Implements a widget that will display a costmap"""
    def __init__(self, costmap, parent = None):
        QtGui.QWidget.__init__(self, parent)
        self.costmap = costmap
        
        # Setup display
        self.imshow = imshow(self.costmap.data.T, interpolation='nearest')
        self.figure = gcf()
        self.image_label = QtGui.QLabel()
        self.image_label.setBackgroundRole(QtGui.QPalette.Base)
        
        # Setup layout
        layout = QtGui.QVBoxLayout()
        layout.addWidget(self.image_label)
        self.setLayout(layout)
        
        # Idle control
        self.idle = True
        
        # Make Qt Connections
        self.connect_stuff()
        
        # Override costmap on change
        self.costmap.on_update = self.costmap_update_callback
    
    def paintEvent(self, vent):
        """Overrides the default paint event"""
        self.figure = gcf()
        # Render the canvas
        self.figure.canvas.draw()
        # Convert the render into a string buffer
        str_buffer = self.figure.canvas.buffer_rgba(0,0)
        # Get the bounding box of the render
        l,b,w,h = self.figure.bbox.bounds
        # Create and set the Pixmap from the render
        image = QtGui.QImage(str_buffer, w, h, QtGui.QImage.Format_ARGB32)
        self.image_label.setPixmap(QtGui.QPixmap.fromImage(image))
    
    def connect_stuff(self):
        """Make Qt connections"""
        self.costmap_changed.connect(self.on_map_update)
    
    def costmap_update_callback(self, key, val):
        """Callback to handle when the map is updated"""
        if self.idle:
            self.idle = False
            self.costmap_changed.emit()
    
    def on_map_update(self):
        """Slot to handle the costmap_changed signal"""
        self.imshow.set_array(self.costmap.data.T)
        print type(self.imshow)
        self.repaint()
        print('Should be repainting')
        self.idle = True
    

def _run_brushfire(c):
    """Runs the brushfire"""
    from brushfire import BrushfireExpansion
    be = BrushfireExpansion(c)
    be.set_ignition_cells([(0,0)])
    import time
    while be.step_solution():
        pass
        # time.sleep(0.1)

def _run_voronoi_expansion(c):
    """Runs the voronoi expansion"""
    from voronoi import VoronoiExpansion
    ve = VoronoiExpansion(c)
    import time
    while ve.step_solution():
        pass
        time.sleep(0.1)

if __name__ == '__main__':
    try:
        c = Costmap2D(10,20,resolution=0.1)
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
