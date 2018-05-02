import pyglet
import serial
import numpy as np
import pandas as pd
import ratcave as rc
from struct import unpack

def connect_to_device(port=None, baudrate=None):
    """Connect to Arduino board
    Input:
            - port
            - baudrate
    returns:
    """
    if (port is None) or (baudrate is None):
        raise ValueError("Specify both port and baudrate for the communication channel.")

    PORT = port
    BAUDRATE = baudrate
    print('Connecting...')
    device = serial.Serial(PORT, baudrate=BAUDRATE, timeout=2.)
    device.readline()
    print('Connection successful!')
    return device


class Experiment(object):

    def __init__(self, trials=20, device=None):
        """ Initialize an experiment object

        Inputs:
                - trials: number of trials
                - filename: name for the recorded data
                - path: path for saving the recorded data (if not given it will be saved in current directory)


        """
        self.trials = trials
        self.device = device

        if self.device is None:
            raise ValueError("Don't forget to attach it with a recording device!")

    def create_window(self, screen_ind=0, *args, **kwargs):
        """
        create a window(app) for the experiment
        """

        platform = pyglet.window.get_platform()
        display = platform.get_default_display()
        screen = display.get_screens()[screen_ind]
        self._mywin = pyglet.window.Window(screen=screen, *args, **kwargs)
        self._fr = pyglet.window.FPSDisplay(self._mywin)

    def create_stim(self, type='Plane'):
        self.stim = rc.WavefrontReader(rc.resources.obj_primitives).get_mesh(type, drawmode=rc.POINTS)

    def _save_data(self, data, filename, path):
        dd = np.array(data).reshape(-1, 3)
        df = pd.DataFrame(data=dd, columns=['Time', "Chan1", 'Trial'])
        df.to_csv('../Measurements/' + filename + '.csv', index=False)

    def run(self, mode='display', on_width=.5, off_width=.5):
        """ runs the experiment in the passed application window

        Input:

        return:

        """

        if type(on_width) == float:
            on_width = [on_width] * 2
        elif len(on_width)>2:
            raise ValueError("on_width must have either on or two values!")

        if type(off_width) == float:
            off_width = [off_width] * 2
        elif len(off_width)>2:
            raise ValueError("off_width must have either on or two values!")

        self.data = []
        self.__trial = 0
        self.__last_trial = self.__trial

        @self._mywin.event
        def on_draw():
            self._mywin.clear()
            with rc.default_shader:
                self.stim.draw()
                if self.__last_trial != self.__trial:
                    self.__last_trial = self.__trial
                    self.device.write(b'S')


        def start_next_trial(dt):
            self.__trial += 1
            self.stim.visible = True
            pyglet.clock.schedule_once(end_trial, np.random.uniform(low=on_width[0], high=on_width[1]))
        pyglet.clock.schedule_once(start_next_trial, 0)


        def end_trial(dt):
            POINTS = 240
            self.stim.visible = False
            dd = unpack('<' + 'I2H' * POINTS, self.device.read(8 * POINTS))
            self.data.extend(dd)
            if self.__trial > self.trials:
                pyglet.app.exit()  # exit the pyglet app
                self.device.close()  # close the serial communication channel
            pyglet.clock.schedule_once(start_next_trial, np.random.uniform(low=off_width[0], high=off_width[1]))


        def update(dt):
            pass
        pyglet.clock.schedule(update)

        pyglet.app.run()


    def save(self, filename=None, path=None):
        """
        to save the recorded data while runing the experiment

        Inputs:
                -

        Returns:
                -
        """

        # Checking the necessary inputs
        if filename is None:
            raise ValueError("Specify a name for the recorded data")

        if path is None:
            # set the path to the current path
            pass