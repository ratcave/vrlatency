import pyglet
pyglet.options['debug_gl'] = False
pyglet.options['debug_gl_trace'] = False
import serial
import numpy as np
import pandas as pd
import ratcave as rc
from struct import unpack

import click
import functools


def common_params(func):
    # arduino specific inputs
    @click.option('--port', default='COM9', help="Port that Arduino board is connected to")
    @click.option('--baud', default=250000, help="Serial communication baudrate")
    # experiment specific inputs
    @click.option('--trials', default=0, help="number of trials for measurement")
    # specify the path to save the data in
    # @click.option('--save_data_in', default=None, help="The path within which the measurement data is saved")
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        return func(*args, **kwargs)
    return wrapper


@click.command()
@common_params
def disp(port, baud, trials):
    ''' Measuring the display latency. This code works with the Arduino code: display_latency.ino '''

    # create a window and project it on the display of your choice
    platform = pyglet.window.get_platform()
    display = platform.get_default_display()
    screen = display.get_screens()[1]
    mywin = pyglet.window.Window(fullscreen=True, screen=screen, vsync=False)
    fr = pyglet.window.FPSDisplay(mywin)

    # initialize a stim object
    plane = rc.WavefrontReader(rc.resources.obj_primitives).get_mesh('Plane', drawmode=rc.POINTS)
    plane.point_size = 10.
    plane.position.xyz = 0, 0, -3
    plane.rotation.x = 0
    plane.scale.xyz = .2

    # define (and start) the serial connection
    ARDUINO_PORT = port
    BAUDRATE = baud
    print('Connecting...')
    device = serial.Serial(ARDUINO_PORT, baudrate=BAUDRATE, timeout=2.)
    print("Emptying buffer")
    device.readline()

    global trial, last_trial, POINTS, TOTAL_POINTS, data
    trial = 0
    last_trial = trial
    POINTS = 240
    TOTAL_POINTS = 1000000
    data = []

    @mywin.event
    def on_draw():
        mywin.clear()
        with rc.default_shader:
            plane.draw()
            global last_trial
            if last_trial != trial:
                last_trial = trial
                device.write(b'S')


    def save_data(data):
        dd = np.array(data).reshape(-1, 3)
        df = pd.DataFrame(data=dd, columns=['Time', "Chan1", 'Trial'])
        filename = 'testing'
        df.to_csv('../Measurements/' + filename + '.csv', index=False)


    def start_next_trial(dt):
        global trial
        trial += 1
        plane.visible = True
        pyglet.clock.schedule_once(end_trial, .05)
    pyglet.clock.schedule_once(start_next_trial, 0)


    def end_trial(dt):
        plane.visible = False
        dd = unpack('<' + 'I2H' * POINTS, device.read(8 * POINTS))
        data.extend(dd)
        if trial > trials:
            save_data(data)
            pyglet.app.exit()
        pyglet.clock.schedule_once(start_next_trial, np.random.random() / 5 + .1)


    def update(dt):
        pass
    pyglet.clock.schedule(update)

    pyglet.app.run()
    device.close()

@click.command()
@common_params
def total(port, baud, trials):
    click.echo("total latency measurement code!" + " " +  str(port) + " " + str(baud) + " " + str(trials))
	
def tracking(port, baud, trials):
	click.echo("tracking latency measurement code!" + " " +  str(port) + " " + str(baud) + " " + str(trials))