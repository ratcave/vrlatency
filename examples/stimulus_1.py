import vrlatency as vrl
import itertools
import pyglet
from time import sleep

# initialize a window
platform = pyglet.window.get_platform()
display = platform.get_default_display()
screen = display.get_screens()[1]
mywin = pyglet.window.Window(fullscreen=True, screen=screen)

# initialize a stimulus object
mypoint = vrl.Stimulus(position=(mywin.width//2, mywin.height//2), size=10)

pos_x = itertools.cycle([mywin.width//2 - 200, mywin.width//2 + 200])
colors = itertools.cycle([(255, 0, 0), (0, 255, 0)])

while not mywin.has_exit:
    mywin.dispatch_events()

    mypoint.position = next(pos_x), mywin.height//2
    mypoint.color = next(colors)
    mywin.clear()
    mypoint.draw()
    mywin.flip()
    sleep(.1)
