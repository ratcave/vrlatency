from abc import abstractmethod
import pyglet
import serial
import numpy as np
# import pandas as pd
import ratcave as rc
import VRLatency as vrl
from struct import unpack

# from Stimulus import *

class Device(object):
    """ Handles attributes and methods related to stimulation/recording device

    Attributes:
        channel:
        is_connected (bool):

    """

    def __init__(self, port='COM9', baudrate=250000):
        self.port = port
        self.baudrate = baudrate
        self.channel = serial.Serial(self.port, baudrate=self.baudrate, timeout=2.)
        self.channel.readline()

    @staticmethod
    def find_device():
        """ Display a list of connected devices to the machine

        Returns:
            list of the ports and the connected devices to this machine

        """
        raise NotImplementedError()

    def disconnect(self):
        """Disconnect the device."""
        self.channel.close()

    @property
    def is_connected(self):
        return self.channel.isOpen()


class Window(pyglet.window.Window):
    """ Window object for the experiment

    Attributes:

    """

    def __init__(self, screen_ind=0, resizable=False, fullscreen=False, *args, **kwargs):
        """ initialize window object

        Args:
            screen_ind: inidicate which screen must contain the created window (if you have more than one screen)
            resizable: in case a resizable window is required, set this to True (default is False)
            fullscreen: for a fullscreen window, set this to True (default is False)
            args and kwargs: all other inputs that pyglet window objects can accept (look into pyglet documentaion)

        """
        platform = pyglet.window.get_platform()
        display = platform.get_default_display()
        screen = display.get_screens()[screen_ind]
        super().__init__(screen=screen, resizable=resizable, fullscreen=fullscreen, *args, **kwargs)


class Stim():
    """ initialize an stimulation object

    Attributes:
        mesh: the object appearing on the screen

    """
    def __init__(self, type='Plane', position=(0, 0)):
        self.mesh = rc.WavefrontReader(rc.resources.obj_primitives).get_mesh(type, drawmode=rc.POINTS, position=(0, 0, -3))
        self.position = position

    @property
    def position(self):
        return self.mesh.position.xy

    @position.setter
    def position(self, value):
        self.mesh.position.xy = value

    def draw(self):
        self.mesh.draw()


class Data(object):
    """ Data object handling data-related matters

    Attributes:
        _array: stores the recorded data during the experiment (if record is set to True, and there exist a recording device)

    """

    def __init__(self):

        self._array = []

    @property
    def array(self):
        return self._array

    def record(self):
        raise NotImplementedError()

    def store(self):
        raise NotImplementedError()

        # dd = np.array(data).reshape(-1, 3)
        # df = pd.DataFrame(data=dd, columns=['Time', "Chan1", 'Trial'])
        # df.to_csv('../Measurements/' + filename + '.csv', index=False)

    def analyze(self):
        raise NotImplementedError()


class BaseExperiment(object):
    """ Experiment object integrates other components and let's use to run, record and store experiment data

    """
    def __init__(self, window, device, trials=20, stim=None):
        """ Initialize an experiment object

        Args:
                - trials: number of trials
                - filename: name for the recorded data
                - path: path for saving the recorded data (if not given it will be saved in current directory)
        """

        # create window
        self.device = device
        self.window = window
        self.stim = stim

        # create Data object
        self.data = Data()

        self.trials = trials
        self._trial = 0
        self.__last_trial = self._trial

        self._init_window_events()
    @property
    def trial(self):
        return self._trial

    def _init_window_events(self):
        @self.window.event
        def on_draw():
            self.window.clear()
            with rc.default_shader:
                self.stim.draw()

    def run(self, record=False):
        """ runs the experiment in the passed application window

        Input:

        return:

        """

        if record and (self.device is None):
            self.window.close()
            raise ValueError("No recording device attached.")

        self.paradigm()

        pyglet.clock.schedule(lambda dt: dt)
        pyglet.app.run()

    @abstractmethod
    def paradigm(self):
        pass


class DisplayExperiment(BaseExperiment):

    def __init__(self, window, device, trials=20, stim=None, on_width=.5, off_width=.5):

        # TODO: use generator for on_width and off_width
        super(self.__class__).__init__(window=window, device=device, trials=trials, stim=stim)
        self.on_width = [float(x) for x in on_width] if hasattr(on_width, '__iter__') and len(on_width) == 2 else [float(on_width)] * 2
        self.off_width = off_width

    def paradigm(self):

        # TODO: simplify this bit
        if self.__last_trial != self._trial:
            self.__last_trial = self._trial
            self.device.channel.write(b'S')


        def start_next_trial(dt):
            self._trial += 1
            self.stim.visible = True
            pyglet.clock.schedule_once(end_trial, np.random.uniform(low=on_width[0], high=on_width[1]))
        pyglet.clock.schedule_once(start_next_trial, 0)


        def end_trial(dt):
            POINTS = 240
            self.stim.visible = False
            dd = unpack('<' + 'I2H' * POINTS, self.device.channel.read(8 * POINTS))
            self.data.array.extend(dd)
            if self._trial > self.trials:
                pyglet.app.exit()  # exit the pyglet app
                self.device.channel.close()  # close the serial communication channel
            pyglet.clock.schedule_once(start_next_trial, np.random.uniform(low=off_width[0], high=off_width[1]))



class tracking_latency(BaseExperiment):

    def _init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def paradigm(self):
        raise NotImplementedError()


class total_latency(BaseExperiment):

    def _init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def paradigm(self):
        vrl.Stim_without_tracking(window=self.window, mesh=self.stim.mesh)
        # while len(self.data) < TOTAL_POINTS * 11:
        #     self.data.extend(unpack('<' + 'I3H?' * POINTS, device.read(11 * POINTS)))
