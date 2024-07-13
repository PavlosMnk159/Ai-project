"""
This contains all the bodies needed for the simulation
"""

import pymunk
import pymunk.pygame_util


class Ball:
    def __init__(self, position, radius, space):
        self.location = position
        self.radius = radius
        self.body = pymunk.Body()
        self.body.position = position
        self.shape = pymunk.Circle(self.body, radius)
        self.shape.density = 1
        self.shape.elasticity = 0.5
        space.add(self.body, self.shape)

class Box:
    def __init__(self, location = (100, 100), size = (50, 50), space = None):
        self.size = size
        self.location = location
        self.body = pymunk.Body()
        self.body.position = location
        self.box = pymunk.Poly.create_box(self.body, self.size)
        self.box.density = 1
        self.box.elasticity = 0.5
        space.add(self.body, self.box)

class Segment:
    def __init__(self, start_pos, end_pos, radius, space):
        self.start_pos = start_pos
        self.end_pos = end_pos
        self.radius = radius
        self.body = pymunk.Body()
        self.segment = pymunk.Segment(self.body, start_pos, end_pos, radius)
        self.segment.elasticity = 0.99
        self.segment.density = 1
        space.add(self.body, self.segment)

class Floor:
    def __init__(self,space):
        self.body = pymunk.Body(body_type=pymunk.Body.STATIC)
        self.shape = pymunk.Segment(self.body, (0, 700), (800, 700), 5)
        self.shape.elasticity = 0.5
        space.add(self.body, self.shape)
        

        