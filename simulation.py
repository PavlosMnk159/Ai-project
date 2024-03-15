import pygame
import pymunk
import pymunk.pygame_util

pygame.init()

width = 800
height = 800
clock = pygame.time.Clock()
Fps = 120

display = pygame.display.set_mode((width, height))
space = pymunk.Space()
space.gravity = 0, 800

def convert_coordinates(point):
    return point[0], height - point[1]

class Ball:
    def __init__(self, x, y, radius):
        self.location = (x, y)
        self.radius = radius
        self.body = pymunk.Body()
        self.body.position = x, y
        self.shape = pymunk.Circle(self.body, radius)
        self.shape.density = 1
        self.shape.elasticity = 0.5
        space.add(self.body, self.shape)

    def draw(self):
        pygame.draw.circle(display, (255,0,0), convert_coordinates(self.body.position), self.radius)

class Box:
    def __init__(self, location = (100, 100), size = (50, 50)):
        self.size = size
        self.location = location
        self.body = pymunk.Body()
        self.body.position = location
        self.box = pymunk.Poly.create_box(self.body, self.size)
        self.box.density = 1
        self.box.elasticity = 0.5
        space.add(self.body, self.box)

    def match_coordinates(self, position):
        loc = convert_coordinates(position)
        x = loc[0] - self.size[0] / 2
        y = loc[1] - self.size[1] / 2
        return int(x), int(y)

    def draw(self):
        pygame.draw.rect(display, (0,0,255), (self.match_coordinates(self.body.position), (50, 50)))

class Segment:
    def __init__(self, start_pos, end_pos, radius):
        self.start_pos = start_pos
        self.end_pos = end_pos
        self.radius = radius
        self.body = pymunk.Body()
        self.segment = pymunk.Segment(self.body, start_pos, end_pos, radius)
        self.segment.elasticity = 0.99
        self.segment.density = 1
        space.add(self.body, self.segment)
class Floor:
    def __init__(self):
        self.body = pymunk.Body(body_type=pymunk.Body.STATIC)
        self.shape = pymunk.Segment(self.body, (0, 700), (800, 700), 5)
        self.shape.elasticity = 0.5
        space.add(self.body, self.shape)

class PinJoint:
    def __init__(self, b1, b2, a1=(0, 0), a2=(0, 0)):
        self.b1 = b1
        self.b2 = b2
        self.a1 = a1
        self.a2 = a2
        joint = pymunk.constraints.PinJoint(b1, b2, a1, a2)
        space.add(joint)

    def FixCoords(self, position, anchor):
        x = position[0] + anchor[0]
        y = position[1] + anchor[1]
        return convert_coordinates((x, y))


    def draw(self):
        pygame.draw.line(display, (0,0,0), self.FixCoords(self.b1.position, self.a1), self.FixCoords(self.b2.position, self.a2))

class PivotJoint:
    def __init__(self, b1, b2, a1=(0,0), a2=(0,0)):
        joint = pymunk.constraints.PivotJoint(b1, b2, a1, a2)
        space.add(joint)

class MotorJoint:
    def __init__(self, b1, b2, rate):
        self.joint = pymunk.constraints.SimpleMotor(b1, b2, rate)
        self.joint.max_force = Fps*10000000
        self.joint.max_bias = 1
        self.joint.rate = rate
        space.add(self.joint)

    def SetRate(self, rate):
        self.joint.rate = rate



b0 = space.static_body
# s = Segment((0, 0), (100, 100), 10)

class RagDoll:
    def __init__(self, Position, Size, Limb_radius, Limb_size, Head_size):
        self.Position = Position
        self.Size = Size
        self.Limb_radius = min(Limb_radius, Size[0], Size[1])
        self.Limb_size = min(Limb_size, Size[0], Size[1])
        self.Head_size = min(Head_size, Size[0], Size[1])


#Parameters regarding the dimentions of the body
Position = (500,400)
Size = (50, 100)
Limb_radius = 10
Limb_size = 80
Head_size = 30


'''
------------------------------------------
body parts
------------------------------------------
'''

#the torso is a box whose center we assume is the location of the body
torso = Box(Position, Size)

#the head must be centered with the body on the x axis and on the y axis it is just above the top of the torso
head = Ball(Position[0], Position[1] - (Size[1]//2 + Head_size), Head_size)

#this is the start of the upper arms
#they are located just below the top of the torso (it is offset by the Limb_radius on the y axis)
#on the x axis the are on opposite sides of the torso and outside of it at a distance of Limb_radius
Uarm1_Pos = (Position[0] + (Size[0]//2 + Limb_radius), Position[1] - Size[1]//2 + Limb_radius)
Uarm2_Pos = (Position[0] - (Size[0]//2 + Limb_radius), Position[1] - Size[1]//2 + Limb_radius)

#the segments start at the position mentioned above and extend to a distance of Limb_size on the x axis
Uarm1 = Segment(Uarm1_Pos, (Uarm1_Pos[0] + Limb_size, Uarm1_Pos[1]), Limb_radius)
Uarm2 = Segment(Uarm2_Pos, (Uarm2_Pos[0] - Limb_size, Uarm2_Pos[1]), Limb_radius)


#the position of the lower arms is the position of the upper arm + the upper arms size + the radius of the limbs(so there is clearence)
Larm1_Pos = (Uarm1_Pos[0] + (Limb_size + Limb_radius), Uarm1_Pos[1])
Larm2_Pos = (Uarm2_Pos[0] - (Limb_size + Limb_radius), Uarm2_Pos[1])

#the segments start at the position mentioned above and extend to a distance of Limb_size on the x axis
Larm1 = Segment(Larm1_Pos, (Larm1_Pos[0] + Limb_size, Larm1_Pos[1]), Limb_radius)
Larm2 = Segment(Larm2_Pos, (Larm2_Pos[0] - Limb_size, Larm2_Pos[1]), Limb_radius)


Uleg1_Pos = (Position[0] + (Size[0]//2) - Limb_radius, Position[1] + Size[1]//2 + Limb_radius)
Uleg2_Pos = (Position[0] - (Size[0]//2) + Limb_radius, Position[1] + Size[1]//2 + Limb_radius)

Uleg1 = Segment(Uleg1_Pos, (Uleg1_Pos[0] , Uleg1_Pos[1] + Limb_size), Limb_radius)
Uleg2 = Segment(Uleg2_Pos, (Uleg2_Pos[0] , Uleg2_Pos[1] + Limb_size), Limb_radius)


Lleg1_Pos = (Uleg1_Pos[0] - Limb_radius, Uleg1_Pos[1] + (Limb_size + Limb_radius))
Lleg2_Pos = (Uleg2_Pos[0] - Limb_radius, Uleg2_Pos[1] + (Limb_size + Limb_radius))

Lleg1 = Segment(Lleg1_Pos, (Lleg1_Pos[0], Lleg1_Pos[1] + Limb_size), Limb_radius)
Lleg2 = Segment(Lleg2_Pos, (Lleg2_Pos[0], Lleg2_Pos[1] + Limb_size), Limb_radius)

'''
------------------------------------------
joints
------------------------------------------
'''


#the neck connects the head to the body and the joint is offest so the anchor point is closer to the head and the movement looks better
neck = PinJoint(torso.body, head.body, (0, -Size[1]//2 + Head_size))

#the torso's anchor point is offset so that it is where the shoulder should be on a body and the upper arms anchor point is offset to its current position (idk why but it works)
shoulder1 = PivotJoint(torso.body, Uarm1.body, (Size[0]//2 + Limb_radius, -Size[1]//2 + Limb_radius), Uarm1_Pos)
shoulder2 = PivotJoint(torso.body, Uarm2.body, (-Size[0]//2 - Limb_radius, -Size[1]//2 + Limb_radius), Uarm2_Pos)

#the upper arms's anchor point is offset so that it is where the elbow should be on a body and the lower arms anchor point is offset to its current position (idk why but it works)
eblow1 = PivotJoint(Uarm1.body, Larm1.body, (Larm1_Pos[0] + Limb_radius, Larm1_Pos[1]), Larm1_Pos)
eblow2 = PivotJoint(Uarm2.body, Larm2.body, (Larm2_Pos[0] - Limb_radius, Larm2_Pos[1]), Larm2_Pos)

hip1 = PivotJoint(torso.body, Uleg1.body, (Size[0]//2 - Limb_radius, Size[1]//2 + Limb_radius), Uleg1_Pos)
hip2 = PivotJoint(torso.body, Uleg2.body, (-Size[0]//2 + Limb_radius, Size[1]//2 + Limb_radius), Uleg2_Pos)

knee1 = PivotJoint(Uleg1.body, Lleg1.body, (Lleg1_Pos[0], Lleg1_Pos[1] + Limb_radius), Lleg1_Pos)
knee2 = PivotJoint(Uleg2.body, Lleg2.body, (Lleg2_Pos[0], Lleg2_Pos[1] + Limb_radius), Lleg2_Pos)

'''
Motor joints
'''

mshoulder1 = MotorJoint(torso.body, Uarm1.body, 0)
mshoulder2 = MotorJoint(torso.body, Uarm2.body, 0)

melbow1 = MotorJoint(Uarm1.body, Larm1.body, 0)
melbow2 = MotorJoint(Uarm2.body, Larm2.body, 0)

mhip1 = MotorJoint(torso.body, Uleg1.body, 0)
mhip2 = MotorJoint(torso.body, Uleg2.body, 0)

mknee1 = MotorJoint(Uleg1.body, Lleg1.body, 0)
mknee2 = MotorJoint(Uleg2.body, Lleg2.body, 0)




# j = PivotJoint(b0, s.body, (300, 300))
# j2 = MotorJoint(s.body, b0, 10)
floor = Floor()


draw_options = pymunk.pygame_util.DrawOptions(display)


def main():
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return
                
        display.fill((255, 255, 255))

        space.debug_draw(draw_options)

        
        pygame.display.update() 
        clock.tick(Fps)
        space.step(1/Fps)


            
        
main()
pygame.quit()
