import pyglet
import numpy as np
# import ratcave as rc
from time import sleep
from itertools import cycle
# import natnetclient as natnet

class plane:

    def __init__(self, position=(0, 0), width=1, height=1, color=(255, 0, 0)):

        self._x, self._y = position
        self._width = width
        self._height = height
        self._color = color * 4

        self.vertices = pyglet.graphics.vertex_list(4,
                                                    ('v2i', (self._x - self._width//2, self._y - self._height//2,
                                                             self._x - self._width//2, self._y + self._height//2,
                                                             self._x + self._width//2, self._y + self._height//2,
                                                             self._x + self._width//2, self._y - self._height//2)),
                                                    ('c3B', self._color)
                                                    )
    
    def draw(self):
        self.vertices.draw(pyglet.gl.GL_POLYGON)


class Stimulus:

    def __init__(self, type='PLANE', position=(0, 0), width=1, height=1, color=(255, 255, 255)):

        self.type = type
        self.position = position
        self.width = width
        self.height = height
        self.color = color

    @property
    def position(self):
        return self._position
    
    @position.setter
    def position(self, val):
        self._position = val

    @property
    def width(self):
        return self._width

    @width.setter
    def width(self, val):
        self._width = val

    @property
    def height(self):
        return self._height

    @height.setter
    def height(self, val):
        self._height = val

    @property
    def color(self):
        return self._color

    @color.setter
    def color(self, val):
        self._color = val

    def draw(self):
        
        if self.type == 'PLANE':
            self._obj = plane(position=self.position, width=self.width, height=self.height, color=self.color)
            
        self._obj.draw()


# class Stimulus(object):
#     """ initialize an stimulation object

#     Attributes:
#         mesh: the object appearing on the screen

#     """
#     def __init__(self, type='Plane', color=(1., 1., 1.), position=(0, 0), size=5):
#         self.mesh = rc.WavefrontReader(rc.resources.obj_primitives).get_mesh(type, drawmode=rc.POINTS,
#                                                                              position=(position[0], position[1], -3))
#         self.mesh.uniforms['flat_shading'] = True
#         self.position = position
#         self.color = tuple(color)
#         self.size = size

#     @property
#     def position(self):
#         return self.mesh.position.x, self.mesh.position.y

#     @position.setter
#     def position(self, value):
#         self.mesh.position.x, self.mesh.position.y = value

#     @property
#     def color(self):
#         return self.mesh.uniforms['diffuse']

#     @color.setter
#     def color(self, values):
#         r, g, b = values
#         self.mesh.uniforms['diffuse'] = r, g, b

#     @property
#     def size(self):
#         return self.mesh.point_size

#     @size.setter
#     def size(self, value):
#         self.mesh.point_size = int(value)

#     def draw(self):
#         with rc.default_shader:
#             self.mesh.draw()


# def Stim_without_tracking(window=None, mesh=None):

#     mywin = window
#     mesh = mesh

#     @mywin.event
#     def on_draw():
#         mywin.clear()
#         with rc.default_shader:
#             mesh.draw()

#     pos = cycle([0, .09])
#     def update(dt):
#         sleep_time = np.random.random() / 5 + .05  # random numbers between 50 and 250 ms
#         sleep(sleep_time)
#         mesh.position.x = next(pos)
#     pyglet.clock.schedule(update)

#     pyglet.app.run()

# def Stim_with_tracking(window=None, mesh=None):

#     mywin = window
#     mesh = mesh

#     # initiate a natnet object
#     client = natnet.NatClient()  # read_rate=1000
#     LED = client.rigid_bodies['LED']

#     @mywin.event
#     def on_draw():
#         mywin.clear()
#         with rc.default_shader:
#             mesh.draw()

#     def update(dt):                                    # for 1024x768: 2.9 - 1.2
#         mesh.position.x = -LED.position.x * 1.6 - .39 # for 1920x1080: 1.65 - .388
#         mesh.position.y = LED.position.z - .15

#     pyglet.clock.schedule(update)

#     pyglet.app.run()




