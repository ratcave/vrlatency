import pyglet
import numpy as np
import ratcave as rc
from time import sleep
from itertools import cycle
# import natnetclient as natnet


class Stimulus(object):
    """ initialize an stimulation object

    Attributes:
        mesh: the object appearing on the screen

    """
    def __init__(self, type='Plane', color=(1., 1., 1.), position=(0, 0)):
        self.mesh = rc.WavefrontReader(rc.resources.obj_primitives).get_mesh(type, drawmode=rc.POINTS, position=(0, 0, -3))
        self.position = position
        self.color = tuple(color)

    @property
    def position(self):
        return self.mesh.position.xy

    @position.setter
    def position(self, value):
        self.mesh.position.xy = value

    @property
    def color(self):
        return self.mesh.uniforms['diffuse']

    @color.setter
    def color(self, values):
        r, g, b = values
        self.mesh.uniforms['diffuse'] = r, g, b

    def draw(self):
        with rc.default_shader:
            self.mesh.draw()


def Stim_without_tracking(window=None, mesh=None):

    mywin = window
    mesh = mesh

    @mywin.event
    def on_draw():
        mywin.clear()
        with rc.default_shader:
            mesh.draw()

    pos = cycle([0, .09])
    def update(dt):
        sleep_time = np.random.random() / 5 + .05  # random numbers between 50 and 250 ms
        sleep(sleep_time)
        mesh.position.x = next(pos)
    pyglet.clock.schedule(update)

    pyglet.app.run()

def Stim_with_tracking(window=None, mesh=None):

    mywin = window
    mesh = mesh

    # initiate a natnet object
    client = natnet.NatClient()  # read_rate=1000
    LED = client.rigid_bodies['LED']

    @mywin.event
    def on_draw():
        mywin.clear()
        with rc.default_shader:
            mesh.draw()

    def update(dt):                                    # for 1024x768: 2.9 - 1.2
        mesh.position.x = -LED.position.x * 1.6 - .39 # for 1920x1080: 1.65 - .388
        mesh.position.y = LED.position.z - .15

    pyglet.clock.schedule(update)

    pyglet.app.run()


