import sys
from math import *
import numpy as np

class DifferentialKinematics(object):
    """Kinematics of a differential robot"""
    def __init__(self, track_length, radius, x=0.0, y=0.0, w=0.0):
        """
        track_length is the distance from the center of each wheel to the center of axel. (m)
        radius is the radius of the tires. (m)
        x is the initial position of the robot in the X_I direction. (m)
        y is the initial position of the robot in the Y_I direction. (m)
        w is the initial rotation of the robot in the Inertial (I) frame. (rad)
        """
        self.track_length = track_length
        self.radius = radius
        
        self.x = x
        self.y = y
        self.w = w
        
        self.left_wheel_speed = 0.0
        self.right_wheel_speed = 0.0
        self.linear_velocity = 0.0
        self.angular_velocity = 0.0
    
    def forward(self, left_wheel_speed = None, right_wheel_speed = None):
        """
        This returns (linear_vel, angular_vel) given left and right wheel speed.
        
        left_wheel_speed is the angular velocity of the left wheel of the robot. (rev/s)
        right_wheel_speed is the angular velocity of the right wheel of the robot. (rev/s)
        Returns the linear and angular velocity of the robot in the robot frame (R).
        """
        return (1,2)
    
    def inverse(self, linear_vel, angular_vel):
        """
        This returns (left_wheel_speed, right_wheel_speed) given linear and angular velocity.
        
        linear_vel is the linear velocity in the Robot frame (R). (m/s)
        angular_vel is the angular velocity in the Robot frame (R). (rad/s)
        Returns the left wheel and right wheel speed. (rev/s)
        """
        pass
    
    def stepSimulation(self, time_delta):
        """
        Increments the simulation one step given the time delta to step.
        
        time_delta is the duration of the step in the kinematics simulation. (secs)
        Returns the new (x, y, w) position and orientation of the robot.
        """
        # Calculate updates in the robot frame
        x_r = self.linear_vel * self.time_delta
        y_r = 0.0
        w_r = self.angular_vel * self.time_delta
        
        # Rotate into the Inertial frame
        inverse_rotation_matrix = np.mat([[cos(w_r), -sin(w_r), 0],
                                          [sin(w_r), cos(w_r),  0],
                                          [0,        0,         1]])
        zeta_I = inverse_rotation_matrix * np.mat([[x_r],
                                                   [y_r],
                                                   [w_r]])
        
        # Increment the absolute position in the Inertial frame
        self.x += zeta_I[0]
        self.y += zeta_I[1]
        self.w += zeta_I[2]
        return (self.x, self.y, self.w)
    

if __name__ == '__main__':
    dk = DifferentialKinematics(0.30, 0.15)
