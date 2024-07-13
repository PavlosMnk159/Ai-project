from Bodies import *
from Joints import *

class RagDoll:
    def __init__(self, Position, TorsoSize, Limb_radius, Limb_size, Head_size, space):
        self.Position = Position
        self.TorsoSize = TorsoSize
        Limb_radius = min(Limb_radius, TorsoSize[0], TorsoSize[1])
        Limb_size = min(Limb_size, TorsoSize[0], TorsoSize[1])
        Head_size = min(Head_size, TorsoSize[0], TorsoSize[1])



        '''
        ------------------------------------------
        body parts
        ------------------------------------------
        '''



        #head ---------------------------------------------------------------------------------------------------------------------

        #the head must be centered with the body on the x axis and on the y axis it is just above the top of the torso
        Head_Pos = (Position[0], Position[1] - (TorsoSize[1]//2 + Head_size))

        head = Ball(Head_Pos, Head_size, space)
        


        #torso --------------------------------------------------------------------------------------------------------------------
        
        #the torso is a box whose center we assume is the location of the body
        torso = Box(Position, TorsoSize, space)
        


        #upper arms ---------------------------------------------------------------------------------------------------------------

        #this is the start of the upper arms
        #they are located just below the top of the torso (it is offset by the Limb_radius on the y axis)
        #on the x axis the are on opposite sides of the torso and outside of it at a distance of Limb_radius
        Uarm1_Pos = (Position[0] + (TorsoSize[0]//2 + Limb_radius), Position[1] - TorsoSize[1]//2 + Limb_radius)
        Uarm2_Pos = (Position[0] - (TorsoSize[0]//2 + Limb_radius), Position[1] - TorsoSize[1]//2 + Limb_radius)

        #the segments start at the position mentioned above and extend to a distance of Limb_size on the x axis
        Uarm1 = Segment(Uarm1_Pos, (Uarm1_Pos[0] + Limb_size, Uarm1_Pos[1]), Limb_radius, space)
        Uarm2 = Segment(Uarm2_Pos, (Uarm2_Pos[0] - Limb_size, Uarm2_Pos[1]), Limb_radius, space)



        #lower arms ---------------------------------------------------------------------------------------------------------------

        #the position of the lower arms is the position of the upper arm + the upper arms size + the radius of the limbs(so there is clearence)
        Larm1_Pos = (Uarm1_Pos[0] + (Limb_size + Limb_radius), Uarm1_Pos[1])
        Larm2_Pos = (Uarm2_Pos[0] - (Limb_size + Limb_radius), Uarm2_Pos[1])

        #the segments start at the position mentioned above and extend to a distance of Limb_size on the x axis
        Larm1 = Segment(Larm1_Pos, (Larm1_Pos[0] + Limb_size, Larm1_Pos[1]), Limb_radius, space)
        Larm2 = Segment(Larm2_Pos, (Larm2_Pos[0] - Limb_size, Larm2_Pos[1]), Limb_radius, space)



        #upper legs ---------------------------------------------------------------------------------------------------------------

        #this is the start of the upper legs
        #they are located just before the end of the torso to the right and to the left respectively (it is offset by the Limb_radius on the x axis)
        #on the y axis they are just below the torso, at a distance of Limb_radius
        Uleg1_Pos = (Position[0] + (TorsoSize[0]//2) - Limb_radius, Position[1] + TorsoSize[1]//2 + Limb_radius)
        Uleg2_Pos = (Position[0] - (TorsoSize[0]//2) + Limb_radius, Position[1] + TorsoSize[1]//2 + Limb_radius)

        Uleg1 = Segment(Uleg1_Pos, (Uleg1_Pos[0] , Uleg1_Pos[1] + Limb_size), Limb_radius, space)
        Uleg2 = Segment(Uleg2_Pos, (Uleg2_Pos[0] , Uleg2_Pos[1] + Limb_size), Limb_radius, space)



        #lower legs ---------------------------------------------------------------------------------------------------------------


        Lleg1_Pos = (Uleg1_Pos[0] - Limb_radius, Uleg1_Pos[1] + (Limb_size + Limb_radius))
        Lleg2_Pos = (Uleg2_Pos[0] - Limb_radius, Uleg2_Pos[1] + (Limb_size + Limb_radius))

        Lleg1 = Segment(Lleg1_Pos, (Lleg1_Pos[0], Lleg1_Pos[1] + Limb_size), Limb_radius, space)
        Lleg2 = Segment(Lleg2_Pos, (Lleg2_Pos[0], Lleg2_Pos[1] + Limb_size), Limb_radius, space)





        '''
        ------------------------------------------
        joints
        ------------------------------------------
        '''


        #the neck connects the head to the body and the joint is offest so the anchor point is closer to the head and the movement looks better
        neck = PinJoint(torso.body, head.body, (0, -self.TorsoSize[1]//2 + Head_size), (0,0), space)

        #the torso's anchor point is offset so that it is where the shoulder should be on a body and the upper arms anchor point is offset to its current position (idk why but it works)
        shoulder1 = PivotJoint(space, torso.body, Uarm1.body, (self.TorsoSize[0]//2 + Limb_radius, -self.TorsoSize[1]//2 + Limb_radius), Uarm1_Pos)
        shoulder2 = PivotJoint(space, torso.body, Uarm2.body, (-self.TorsoSize[0]//2 - Limb_radius, -self.TorsoSize[1]//2 + Limb_radius), Uarm2_Pos)

        #the upper arms's anchor point is offset so that it is where the elbow should be on a body and the lower arms anchor point is offset to its current position (idk why but it works)
        eblow1 = PivotJoint(space, Uarm1.body, Larm1.body, (Larm1_Pos[0] + Limb_radius, Larm1_Pos[1]), Larm1_Pos)
        eblow2 = PivotJoint(space, Uarm2.body, Larm2.body, (Larm2_Pos[0] - Limb_radius, Larm2_Pos[1]), Larm2_Pos)

        hip1 = PivotJoint(space, torso.body, Uleg1.body, (self.TorsoSize[0]//2 - Limb_radius, self.TorsoSize[1]//2 + Limb_radius), Uleg1_Pos)
        hip2 = PivotJoint(space, torso.body, Uleg2.body, (-self.TorsoSize[0]//2 + Limb_radius, self.TorsoSize[1]//2 + Limb_radius), Uleg2_Pos)

        knee1 = PivotJoint(space, Uleg1.body, Lleg1.body, (Lleg1_Pos[0], Lleg1_Pos[1] + Limb_radius), Lleg1_Pos)
        knee2 = PivotJoint(space, Uleg2.body, Lleg2.body, (Lleg2_Pos[0], Lleg2_Pos[1] + Limb_radius), Lleg2_Pos)





        '''
        Motor joints
        '''

        mshoulder1 = MotorJoint(torso.body, Uarm1.body, 0, space)
        mshoulder2 = MotorJoint(torso.body, Uarm2.body, 0, space)

        melbow1 = MotorJoint(Uarm1.body, Larm1.body, 0, space)
        melbow2 = MotorJoint(Uarm2.body, Larm2.body, 0, space)

        mhip1 = MotorJoint(torso.body, Uleg1.body, 0, space)
        mhip2 = MotorJoint(torso.body, Uleg2.body, 0, space)

        mknee1 = MotorJoint(Uleg1.body, Lleg1.body, 0, space)
        mknee2 = MotorJoint(Uleg2.body, Lleg2.body, 0, space)