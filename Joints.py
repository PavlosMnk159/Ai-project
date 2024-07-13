"""
This contains all the joints needed for the simulation
"""

import pymunk
import pymunk.pygame_util

class PinJoint:
    def __init__(self, body1, body2, anchor1=(0, 0), anchor2=(0, 0), space = None):
        joint = pymunk.constraints.PinJoint(body1, body2, anchor1, anchor2)
        space.add(joint)

class PivotJoint:
    def __init__(self, space, b1, b2, a1=(0,0), a2=(0,0)):
        joint = pymunk.constraints.PivotJoint(b1, b2, a1, a2)
        space.add(joint)

class MotorJoint:
    def __init__(self, b1, b2, rate, space):
        self.joint = pymunk.constraints.SimpleMotor(b1, b2, rate)
        self.joint.max_force = 100000000
        self.joint.max_bias = 1
        self.joint.rate = rate
        space.add(self.joint)

    def SetRate(self, rate):
        self.joint.rate = rate