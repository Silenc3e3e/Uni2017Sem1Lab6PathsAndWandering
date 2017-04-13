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
    elif symbol == KEY.N:
        world.next = True
    elif symbol == KEY.A:
        add_agent()
    elif symbol == KEY.T:
        count = 0
        while count < 10:
            count += 1
            add_agent()
    # LAB 06 TASK 1: Reset all paths to new random ones
    elif symbol == KEY.R:
        for agent in world.agents:
            agent.randomise_path()
    # Toggle debug force line info on the agent
    elif symbol == KEY.I:
        for agent in world.agents:
            agent.show_info = not agent.show_info
    elif symbol == KEY.L:
        GoTo = not world.agents[0].loop
        for agent in world.agents:
            agent.loop = GoTo
    elif symbol in AGENT_MODES:
        for agent in world.agents:
            agent.mode = AGENT_MODES[symbol]
    elif symbol == KEY.Q:
        for agent in world.agents:
            agent.max_force -= 10.0 * agent.floatScale
    elif symbol == KEY.W:
        for agent in world.agents:
            agent.max_force += 10.0 * agent.floatScale

def add_agent():
    newAgent = Agent(world, world.hunter.floatScale, world.hunter.mass/world.hunter.floatScale,'seek',
        world.hunter.friction/world.hunter.floatScale, world.hunter.panicDist/world.hunter.floatScale,
        world.hunter.max_speed/world.hunter.floatScale, world.hunter.waypoint_threshold/world.hunter.floatScale, world.hunter.loop,
        world.hunter.wander_dist/world.hunter.floatScale, world.hunter.wander_radius/world.hunter.floatScale,
        world.hunter.wander_jitter/world.hunter.floatScale, world.hunter.show_info)
    world.agents.append(newAgent)
    world.hunter = newAgent

def on_resize(cx, cy):
    world.cx = cx
    world.cy = cy
def render_stats(world):
    egi.text_color((1.0, 1.0, 1.0, 1))
    depthy = -40
    egi.text_at_pos(10, depthy, 'Game Scale = ' + str(world.hunter.floatScale))
    egi.text_at_pos(10, depthy-20, 'Max Speed = ' + str(world.hunter.max_speed/world.hunter.floatScale))
    egi.text_at_pos(10, depthy-40, 'Max Force = ' + str(world.hunter.max_force/world.hunter.floatScale))
    egi.text_at_pos(10, depthy-60, 'Mass = ' + str(world.hunter.mass/world.hunter.floatScale))
    egi.text_at_pos(10, depthy-80, 'Friction = ' + str(world.hunter.friction/world.hunter.floatScale))
    egi.text_at_pos(10, depthy-100, 'Panic Distance = ' + str(world.hunter.panicDist/world.hunter.floatScale))
    egi.text_at_pos(10, depthy-130, 'Waypoint Threshold = ' + str(world.hunter.waypoint_threshold/world.hunter.floatScale))
    egi.text_at_pos(10, depthy-150, 'Waypoint Loop = ' + str(world.hunter.loop))
    egi.text_at_pos(10, depthy-180, 'Wander Distance = ' + str(world.hunter.wander_dist/world.hunter.floatScale))
    egi.text_at_pos(10, depthy-200, 'Wander radius = ' + str(world.hunter.wander_radius/world.hunter.floatScale))
    egi.text_at_pos(10, depthy-220, 'Wander jitter = ' + str(world.hunter.wander_jitter/world.hunter.floatScale))


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

