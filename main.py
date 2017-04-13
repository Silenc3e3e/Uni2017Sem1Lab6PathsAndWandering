'''Autonomous Agent Movement: Seek, Arrive and Flee

Created for COS30002 AI for Games, Lab 05
By Clinton Woodward cwoodward@swin.edu.au

'''
from graphics import egi, KEY
from pyglet import window, clock
from pyglet.gl import *

from vector2d import Vector2D
from world import World
from agent import Agent, AGENT_MODES  # Agent with seek, arrive, flee and pursuit


def on_mouse_press(x, y, button, modifiers):
    if button == 1:  # left
        world.target = Vector2D(x, y)

def on_key_press(symbol, modifiers):
    if symbol == KEY.P:
        world.paused = not world.paused
    elif symbol == KEY._0:
        world.next = True
    elif symbol == KEY.G:
        add_agent()
    elif symbol == KEY.T:
        count = 0
        while count < 10:
            count += 1
            add_agent()
    # LAB 06 TASK 1: Reset all paths to new random ones
    elif symbol == KEY.O:
        for agent in world.agents:
            agent.randomise_path()
    # Toggle debug force line info on the agent
    elif symbol == KEY.B:
        for agent in world.agents:
            agent.show_info = not agent.show_info
    elif symbol == KEY.I:
        GoTo = not world.agents[0].loop
        for agent in world.agents:
            agent.loop = GoTo
    elif symbol in AGENT_MODES:
        for agent in world.agents:
            agent.mode = AGENT_MODES[symbol]
    #SCALE
    elif symbol == KEY.Q:
        for agent in world.agents:
            if agent.floatScale > 1.0:
                agent.floatScale -= 1.0
    elif symbol == KEY.W:
        for agent in world.agents:
            agent.floatScale += 1.0
    #MAX SPEED
    elif symbol == KEY.E:
        for agent in world.agents:
            if agent.max_speed > 5.0:
                agent.max_speed -= 5.0
    elif symbol == KEY.R:
        for agent in world.agents:
            agent.max_speed += 5.0
    #MAX FORCE
    elif symbol == KEY.A:
        for agent in world.agents:
            if agent.max_force > 5.0:
                agent.max_force -= 5.0
    elif symbol == KEY.S:
        for agent in world.agents:
            agent.max_force += 5.0
    #MASS
    elif symbol == KEY.D:
        for agent in world.agents:
            if agent.mass > 0.1:
                agent.mass -= 0.1
    elif symbol == KEY.F:
        for agent in world.agents:
            agent.mass += 0.1
    #FRICTION
    elif symbol == KEY.Z:
        for agent in world.agents:
            if agent.friction > 0.01:
                agent.friction -= 0.01
    elif symbol == KEY.X:
        for agent in world.agents:
            agent.friction += 0.01
    #PANIC DISTANCE
    elif symbol == KEY.C:
        for agent in world.agents:
            if agent.panicDist > 5:
                agent.panicDist -= 5
    elif symbol == KEY.V:
        for agent in world.agents:
            agent.panicDist += 5
    #WAYPOINT THRESHOLD
    elif symbol == KEY.Y:
        for agent in world.agents:
            if agent.waypoint_threshold > 5:
                agent.waypoint_threshold -= 5
    elif symbol == KEY.U:
        for agent in world.agents:
            agent.waypoint_threshold += 5
    #WANDER DISTANCE
    elif symbol == KEY.H:
        for agent in world.agents:
            if agent.wander_dist > 0.25:
                agent.wander_dist -= 0.25
    elif symbol == KEY.J:
        for agent in world.agents:
            agent.wander_dist += 0.25
    #WANDER RADIUS
    elif symbol == KEY.K:
        for agent in world.agents:
            if agent.wander_radius > 0.25:
                agent.wander_radius -= 0.25
    elif symbol == KEY.L:
        for agent in world.agents:
            agent.wander_radius += 0.25
    #WANDER JITTER
    elif symbol == KEY.N:
        for agent in world.agents:
            if agent.wander_jitter > 0.5:
                agent.wander_jitter -= 0.5
    elif symbol == KEY.M:
        for agent in world.agents:
            agent.wander_jitter += 0.5

def add_agent():
    newAgent = Agent(world, world.hunter.floatScale, world.hunter.mass,'seek',
        world.hunter.friction, world.hunter.panicDist,
        world.hunter.max_speed, world.hunter.waypoint_threshold, world.hunter.loop,
        world.hunter.wander_dist, world.hunter.wander_radius,
        world.hunter.wander_jitter, world.hunter.show_info, world.hunter.max_force)
    world.agents.append(newAgent)
    world.hunter = newAgent

def on_resize(cx, cy):
    world.cx = cx
    world.cy = cy
def render_stats(world):
    egi.text_color((1.0, 1.0, 1.0, 1))
    depthy = -40
    egi.text_at_pos(10, depthy, '(Q/W) Game Scale = ' + str(world.hunter.floatScale))
    egi.text_at_pos(10, depthy-20, '(E/R) Max Speed = ' + str(world.hunter.max_speed))#TODO remove divides
    egi.text_at_pos(10, depthy-40, '(A/S) Max Force = ' + str(world.hunter.max_force))
    egi.text_at_pos(10, depthy-60, '(D/F) Mass = ' + str(world.hunter.mass))
    egi.text_at_pos(10, depthy-80, '(Z/X) Friction = ' + str(world.hunter.friction))
    egi.text_at_pos(10, depthy-100, '(C/V) Panic Distance = ' + str(world.hunter.panicDist))
    egi.text_at_pos(10, depthy-130, '(Y/U) Waypoint Threshold = ' + str(world.hunter.waypoint_threshold))
    egi.text_at_pos(10, depthy-150, '(I) Waypoint Loop = ' + str(world.hunter.loop))
    egi.text_at_pos(10, depthy-170, '(O) Randomize Path')
    egi.text_at_pos(10, depthy-200, '(H/J) Wander Distance = ' + str(world.hunter.wander_dist))
    egi.text_at_pos(10, depthy-220, '(K/L) Wander radius = ' + str(world.hunter.wander_radius))
    egi.text_at_pos(10, depthy-240, '(N/M) Wander jitter = ' + str(world.hunter.wander_jitter))
    egi.text_at_pos(10, depthy-270, '(B) Show agent info')
    egi.text_at_pos(10, depthy-290, '(P) Pause')
    egi.text_at_pos(10, depthy-310, '(0) Next frame (while paused)')


if __name__ == '__main__':

    # create a pyglet window and set glOptions
    win = window.Window(width=1000, height=1000, vsync=True, resizable=True)
    glEnable(GL_BLEND)
    glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)
    # needed so that egi knows where to draw
    egi.InitWithPyglet(win)
    # prep the fps display
    fps_display = clock.ClockDisplay()
    # register key and mouse event handlers
    win.push_handlers(on_key_press)
    win.push_handlers(on_mouse_press)
    win.push_handlers(on_resize)

    # create a world for agents
    world = World(500, 500)
    # add two agents (first one is done manually so default agent values are entered)
    newAgent = Agent(world)
    world.agents.append(newAgent)
    world.hunter = newAgent
    add_agent()
    # unpause the world ready for movement
    world.paused = False

    while not win.has_exit:
        win.dispatch_events()
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        # show nice FPS bottom right (default)
        delta = clock.tick()
        world.update(delta)
        world.render()
        render_stats(world)
        fps_display.draw()
        # swap the double buffer
        win.flip()

