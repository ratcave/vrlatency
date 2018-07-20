import pyglet
import numpy as np
# import ratcave as rc
from time import sleep
from itertools import cycle
# import natnetclient as natnet


class Stimulus:

    def __init__(self, position=(0, 0), color=(255, 255, 255), size=1):

        self.position = position
        self.color = color
        self.size = size

    def draw(self):
        vertices = pyglet.graphics.vertex_list(1, ('v2i', self.position), ('c3B', self.color))

        pyglet.gl.glPointSize(self.size)
        vertices.draw(pyglet.gl.GL_POINTS)
