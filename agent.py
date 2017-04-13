'''An agent with Seek, Flee, Arrive, Pursuit behaviours

Created for COS30002 AI for Games by Clinton Woodward cwoodward@swin.edu.au

'''

from vector2d import Vector2D
from vector2d import Point2D
from graphics import egi, KEY
from math import sin, cos, radians
from random import random, randrange

AGENT_MODES = {
    KEY._1: 'seek',
    KEY._2: 'arrive_slow',
    KEY._3: 'arrive_normal',
    KEY._4: 'arrive_fast',
    KEY._5: 'flee',
    KEY._6: 'pursuit'
}
class DummyAgent(object):
    def __init__(self, x, y):
        self.pos = Vector2D (x, y)
        self.vel = Vector2D(0, 0)

class Agent(object):

    # NOTE: Class Object (not *instance*) variables!
    DECELERATION_SPEEDS = {
        'slow': 0.1,
        'normal': .5,
        'fast': 2,
    }

    def __init__(self, world=None, scale=30.0, mass=2.0, mode='seek', friction = 0.01):
        # keep a reference to the world object
        self.world = world
        self.mode = mode
        # where am i and where am i going? random
        dir = radians(random()*360)
        self.pos = Vector2D(randrange(world.cx), randrange(world.cy))
        self.vel = Vector2D()
        self.heading = Vector2D(sin(dir), cos(dir))
        self.side = self.heading.perp()
        self.scale = Vector2D(scale, scale)  # easy scaling of agent size
        self.force = Vector2D()
        self.accel = Vector2D()  # current steering force
        self.mass = mass
        self.friction = friction

        self.hunterTargVec = Vector2D(10,10)
        self.panicDist = 350
        self.hunterTarg = None

        # limits?
        self.max_speed = 40.0 * scale
        ## max_force ??

        # data for drawing this agent
        self.color = 'ORANGE'
        self.vehicle_shape = [
            Point2D(-1.0,  0.6),
            Point2D( 1.0,  0.0),
            Point2D(-1.0, -0.6)
        ]
        self.hunter_shape = [
            Point2D(-1.0,  0.6),
            Point2D( 0.9,  0.5),
            Point2D( 0.65,  0.4),
            Point2D( 1.1,  0.15),
            Point2D( 0.65,  0.0),
            Point2D( 1.1, -0.15),
            Point2D( 0.65, -0.4),
            Point2D( 0.9, -0.5),
            Point2D(-1.0, -0.6)
        ]

        ### path to follow?
        # self.path = ??

        ### wander details
        # self.wander_?? ...

        # debug draw info?
        self.show_info = False

    def calculate(self):
        # reset the steering force
        mode = self.mode
        if mode == 'seek':
            force = self.seek(self.world.target)
        elif mode == 'arrive_slow':
            force = self.arrive(self.world.target, 'slow')
        elif mode == 'arrive_normal':
            force = self.arrive(self.world.target, 'normal')
        elif mode == 'arrive_fast':
            force = self.arrive(self.world.target, 'fast')
        elif mode == 'flee':
            if self.world.hunter != self:
                force = self.flee(self.world.hunter.pos)
            elif self.world.hunter == self:
                totalx = 0
                totaly = 0
                for agent in self.world.agents:
                    if agent != self:
                        totalx += agent.pos.x
                        totaly += agent.pos.y
                totalAgents = len(self.world.agents)-1
                totalx = totalx / totalAgents
                totaly = totaly / totalAgents
                dumAgent = DummyAgent(totalx, totaly)
                force = self.pursuit(self.FindClosest(dumAgent))

        elif mode == 'pursuit' and self == self.world.hunter:
            target = self.FindClosest(self)
            if self.hunterTarg != None:
                if (self.hunterTarg.pos - self.pos).length() > self.panicDist * 1.05:
                    if target != self.hunterTarg:
                        if self.hunterTarg != None:
                            self.hunterTarg.mode = 'pursuit'
                        self.hunterTarg = target
                        #target.mode = 'flee'
                else:
                    target = self.hunterTarg
            else:
                self.hunterTarg = target
            target.mode = 'flee'
            force = self.pursuit(target)
        else:
            force = Vector2D()
        self.force = force
        return force

    def update(self, delta):
        ''' update vehicle position and orientation '''
        force = self.calculate()
        ## limit force? <-- for wander
        self.accel = force / self.mass
        # new velocity
        self.vel += self.accel * delta
        # proportional friction
        self.vel = self.vel * (1-(self.friction*(self.vel.length()/self.max_speed)))

        # check for limits of new velocity
        self.vel.truncate(self.max_speed)
        # update position
        self.pos += self.vel * delta
        # update heading is non-zero velocity (moving)
        if self.vel.lengthSq() > 0.00000001:
            self.heading = self.vel.get_normalised()
            self.side = self.heading.perp()
        # treat world as continuous space - wrap new position if needed
        self.world.wrap_around(self.pos)

    def render(self, color=None):
        # draw the path if it exists and the mode is follow
        if self.mode == 'follow_path':
            ## ...
            pass

        ''' Draw the triangle agent with color'''
        color = None
        shape = None
        if(self != self.world.hunter):
            color = self.color
            shape = self.vehicle_shape
        else:
            color = 'RED'
            shape = self.hunter_shape
        egi.set_pen_color(name=color)
        pts = self.world.transform_points(shape, self.pos, self.heading, self.side, self.scale)
        # draw it!
        egi.closed_shape(pts)
        if ((self.mode == 'pursuit' or self.mode == 'flee') and self == self.world.hunter):
            egi.green_pen()
            if self.hunterTargVec.y > self.world.cy:
                self.hunterTargVec = Vector2D(self.hunterTargVec.x, self.world.cy)
            elif self.hunterTargVec.y < 0:
                self.hunterTargVec = Vector2D(self.hunterTargVec.x, 0)
            if self.hunterTargVec.x > self.world.cx:
                self.hunterTargVec = Vector2D(self.world.cx, self.hunterTargVec.y)
            elif self.hunterTargVec.x < 0:
                self.hunterTargVec = Vector2D(0, self.hunterTargVec.y)
            egi.cross(self.hunterTargVec, 10)

        # draw wander info?
        if self.mode == 'wander':
            ## ...
            pass

        # add some handy debug drawing info lines - force and velocity
        if self.show_info:
            s = 0.5 # <-- scaling factor
            # force
            egi.red_pen()
            egi.line_with_arrow(self.pos, self.pos + self.force * s, 5)
            # velocity
            egi.grey_pen()
            egi.line_with_arrow(self.pos, self.pos + self.vel * s, 5)
            # net (desired) change
            egi.white_pen()
            egi.line_with_arrow(self.pos+self.vel * s, self.pos+ (self.force+self.vel) * s, 5)
            egi.line_with_arrow(self.pos, self.pos+ (self.force+self.vel) * s, 5)
    def speed(self):
        return self.vel.length()

    #--------------------------------------------------------------------------

    def seek(self, target_pos):
        ''' move towards target position '''
        desired_vel = (target_pos - self.pos).normalise() * self.max_speed
        return (desired_vel - self.vel)

    def flee(self, hunter_pos):
        ''' move away from hunter position '''
        if (hunter_pos - self.pos).length() < self.panicDist:
            desired_vel = -((hunter_pos - self.pos).normalise() * self.max_speed)
            return (desired_vel - self.vel)
        return Vector2D(0, 0)

    def arrive(self, target_pos, speed):
        ''' this behaviour is similar to seek() but it attempts to arrive at
            the target position with a zero velocity'''
        decel_rate = self.DECELERATION_SPEEDS[speed]
        to_target = target_pos - self.pos
        dist = to_target.length()
        if dist > 0:
            # calculate the speed required to reach the target given the
            # desired deceleration rate
            speed = dist / decel_rate
            # make sure the velocity does not exceed the max
            speed = min(speed, self.max_speed)
            # from here proceed just like Seek except we don't need to
            # normalize the to_target vector because we have already gone to the
            # trouble of calculating its length for dist.
            desired_vel = to_target * (speed / dist)
            return (desired_vel - self.vel)
        return Vector2D(0, 0)

    def pursuit(self, evader):
        ''' this behaviour predicts where an agent will be in time T and seeks
            towards that point to intercept it. '''
        target_pos = evader.pos + evader.vel
        #print(str(target_pos.x) + "targetpos")
        self.hunterTargVec = Vector2D(target_pos.x, target_pos.y)
        return (self.arrive(target_pos, 'slow'))

    def wander(self, delta):
        ''' Random wandering using a projected jitter circle. '''
        ## ...
        return Vector2D()

    def FindClosest(self, agentFrom):
        closest = None
        ClosestDistance = 99999999
        for agent in self.world.agents:
            distToAgent = agent.pos.distance(agentFrom.pos)
            if distToAgent < ClosestDistance and agent != self:# and agentToIgnore.pos.x != agentFrom.pos.x and agent.pos.y != agentFrom.pos.y:
                closest = agent
                ClosestDistance = distToAgent
        return closest