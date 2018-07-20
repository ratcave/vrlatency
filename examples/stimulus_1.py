import vrlatency as vrl
import itertools
import pyglet
from time import sleep

mywin = pyglet.window.Window(fullscreen=True)

# initialize a stim object
mypoint = vrl.Stimulus(type='PLANE', position=(mywin.width//2, mywin.height//2), width=50, height=50)

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