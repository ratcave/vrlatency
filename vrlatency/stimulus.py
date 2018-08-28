import pyglet


class Stimulus:

    def __init__(self, position=(0, 0), color=(255, 255, 255), size=100):

        self.position = position
        self.color = color
        self.size = size

    def draw(self):
        vertices = pyglet.graphics.vertex_list(1, ('v2i', self._norm_to_pixel()), ('c3B', self.color))

        pyglet.gl.glPointSize(self.size)
        vertices.draw(pyglet.gl.GL_POINTS)

    def _norm_to_pixel(self):
        """ Returns pixel values for a given normalized stimulus position

        NOTE: if you want the normalization to be between -.5 and .5, rmeove the division by 2 for the self._position.
        Otherwise, the normalization is between -1 and 1.
        """
        pixel_width = self.position[0] / 2 * self.screen.width + self.screen.width / 2
        pixel_height = self.position[1] / 2 * self.screen.height + self.screen.height / 2

        return int(pixel_width), int(pixel_height)
