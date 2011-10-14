#!/usr/bin/env python

import sys
from threading import Thread, Event

from PySide import QtCore, QtGui

from costmapwidget import Costmap2DWidget

DEFAULT_WIDTH = 10
DEFAULT_HEIGHT = 20
DEFAULT_RESOLUTION = 1.0

DEFAULT_TIMEOUT = 0.1

# DEFAULT_DELAY = 0.05
DEFAULT_DELAY = 0.0

class AlgorithmWidget(QtGui.QGroupBox):
    toggle_running_button_state = QtCore.Signal(bool)
    algorithm_finished = QtCore.Signal(bool)
    
    """
    This is a base class for displaying an algorithm.
    
    You should call __init__ and then pack_buttons
    
    You can add widgets to the buttons list before calling 
      pack_buttons to have them added to the HBox under the plot.
    
    You should implement the following abstract functions:
    
    step_solution - This should iterate your algorithm once and 
      return True if more work is to be done and false otherwise.
      
    setup_algorithm - This should create the costmap and algorithm
      objects and prepare them for stepping.
      
    reset_algorithm - This should reset the algorithm.
    
    Here are some signals you might want to know about:
    
    algorithm_finished(bool) - this gets emitted when the algorithm finishes
      with bool = False and when it is reset with bool = True
    """
    def __init__(self, name="Unnamed Algorithm", parent=None):
        QtGui.QGroupBox.__init__(self, name, parent=parent)
        
        self.run_button = QtGui.QPushButton("Run")
        self.step_button = QtGui.QPushButton("Step")
        self.stop_button = QtGui.QPushButton("Stop")
        self.reset_button = QtGui.QPushButton("Reset")
        self.stop_button.setEnabled(False)
        self.buttons = [self.run_button, self.step_button, self.stop_button, self.reset_button]
        
        self.make_connections()
        
        self.algorithm_thread = None
        self.step_event = Event()
        self.stepping = True
        
        self.setup_algorithm()
    
    def hideEvent(self, event):
        """Called when the window is closed (don't know why the closeEvent doesnt work)"""
        self.stop_threading()
        event.accept()
    
    def make_connections(self):
        """Makes the Qt connections"""
        self.run_button.clicked.connect(self.on_run_clicked)
        self.step_button.clicked.connect(self.on_step_clicked)
        self.stop_button.clicked.connect(self.on_stop_clicked)
        self.reset_button.clicked.connect(self.on_reset_clicked)
        
        self.toggle_running_button_state.connect(self.run_button.setEnabled)
        self.toggle_running_button_state.connect(self.step_button.setEnabled)
        self.toggle_running_button_state.connect(self.stop_button.setEnabled)
        self.toggle_running_button_state.connect(self.reset_button.setEnabled)
        
        self.algorithm_finished.connect(self.run_button.setEnabled)
        self.algorithm_finished.connect(self.step_button.setEnabled)
    
    def run_algorithm(self):
        """Runs the algorithm"""
        while self.running:
            self.step_event.wait(DEFAULT_TIMEOUT)
            if self.step_event.is_set():
                if not self.stepping:
                    self.toggle_running_button_state.emit(False)
                result = self.step_solution()
                if not self.stepping:
                    self.toggle_running_button_state.emit(True)
                if not result:
                    self.algorithm_finished.emit(False)
                    self.running = False
                    print 'Algorithm done'
                if self.stepping:
                    self.step_event.clear()
                else:
                    import time
                    if DEFAULT_DELAY: time.sleep(DEFAULT_DELAY)
    
    def setup_algorithm(self):
        """Override this"""
        print '(setup_algorithm) Implement me!'
        from costmap import Costmap2D
        from obstacle import Obstacle
        from costmapwidget import Costmap2DWidget
        self.costmap = Costmap2D(DEFAULT_WIDTH, DEFAULT_HEIGHT, resolution=DEFAULT_RESOLUTION)
        Obstacle(3,3,3,3).draw(self.costmap)
        Obstacle(5,9,3,3).draw(self.costmap)
        Obstacle(4,16,3,3).draw(self.costmap)
        
        self.costmap_widget = Costmap2DWidget(self.costmap, parent = self)
    
    def step_solution(self):
        """Steps the solution (should be overridden) return True if more work to be done"""
        import time, random
        time.sleep(1.0)
        print '(step_solution) Implement me!'
        return True if random.random() < 0.25 else False
    
    def reset_algorithm(self):
        """Override this"""
        print '(reset_algorithm) Implement me!'
    
    def start_threading(self):
        """Starts the algorithm thread"""
        if self.algorithm_thread == None:
            self.reset_algorithm()
            self.algorithm_thread = Thread(target=self.run_algorithm)
            self.running = True
            self.algorithm_thread.start()
    
    def stop_threading(self):
        """Stops the algorithm thread"""
        if self.algorithm_thread != None:
            self.running = False
            self.algorithm_thread.join()
            self.algorithm_thread = None
        if self.step_event.is_set():
            self.step_event.clear()
    
    @QtCore.Slot()
    def on_run_clicked(self):
        """Called when run is clicked"""
        self.start_threading()
        self.stepping = False
        self.step_event.set()
    
    @QtCore.Slot()
    def on_step_clicked(self):
        """Called when step is clicked"""
        self.start_threading()
        self.stepping = True
        self.step_event.set()

    @QtCore.Slot()
    def on_stop_clicked(self):
        """Called when stop is clicked"""
        self.stop_button.setEnabled(False)
        if self.stepping == False:
            self.stepping = True
        self.step_event.set()
    
    @QtCore.Slot()
    def on_reset_clicked(self):
        """Called when reset is clicked"""
        self.stop_threading()
        self.reset_algorithm()
        self.algorithm_finished.emit(True)
    
    def pack_buttons(self):
        """Puts the buttons into the layout, this lets additional buttons to be inserted"""
        button_layout = QtGui.QHBoxLayout()
        for button in self.buttons:
            button_layout.addWidget(button)
        
        layout = QtGui.QVBoxLayout()
        layout.addWidget(self.costmap_widget)
        layout.addLayout(button_layout)
        # layout.addStretch(1)
        self.setLayout(layout)
    
