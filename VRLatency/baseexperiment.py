from abc import abstractmethod
import pyglet
from pyglet.window import key
import serial
import random
import numpy as np
# import pandas as pd
import ratcave as rc
import VRLatency as vrl
from struct import unpack
from itertools import cycle
from warnings import warn
from time import sleep
# import natnetclient as natnet

# from Stimulus import *

class Arduino(object):
    """ Handles attributes and methods related to stimulation/recording device

    Attributes:
        channel:
        is_connected (bool):

    """
    pkt_formats = {'Tracking': 'I2H', 'Display': 'I2H', 'Total': 'I2H'}
    pkt_size = {'Tracking': 8, 'Display': 8, 'Total': 8}
    n_point_options = {'Tracking': 240, 'Display': 240, 'Total': 240}


    def __init__(self, experiment_type, port, baudrate):
        """Can be 'Tracking', 'Display', or 'Total'"""
        self.port = port
        self.baudrate = baudrate
        self.channel = serial.Serial(self.port, baudrate=self.baudrate, timeout=2.)
        self.experiment_type = experiment_type
        self.packet_fmt = self.pkt_formats[experiment_type]
        self.packet_size = self.pkt_size[experiment_type]
        self.n_points = self.n_point_options[experiment_type]
        self.channel.readline()

    @staticmethod
    def find_all():
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

    def read(self, n_points=240):
        return unpack('<' + self.packet_fmt * self.n_points, self.channel.read(self.packet_size * self.n_points))

    def init_next_trial(self):
        self.channel.write(bytes('S', 'utf-8'))

    def ping(self):
        """Returns True if Arduino is connected and has correct code loaded."""
        self.channel.readline()
        self.channel.write(bytes('are_you_ready?', 'utf-8'))
        packet = self.channel.read(30)
        response = unpack('<3c', packet)
        return True if response == 'yes' else False


class Stim(object):
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


class Data(object):
    """ Data object handling data-related matters

    Attributes:
        _array: stores the recorded data during the experiment (if record is set to True, and there exist a recording device)

    """

    def __init__(self):
        self.values = []

    def to_csv(self):
        raise NotImplementedError()

        # dd = np.array(data).reshape(-1, 3)
        # df = pd.DataFrame(data=dd, columns=['Time', "Chan1", 'Trial'])
        # df.to_csv('../Measurements/' + filename + '.csv', index=False)

    def analyze(self):
        raise NotImplementedError()


class BaseExperiment(pyglet.window.Window):
    """ Experiment object integrates other components and let's use to run, record and store experiment data

    """
    def __init__(self, arduino=None, screen_ind=0, trials=20, stim=None, on_width=.5, off_width=.5, *args, **kwargs):
        """ Initialize an experiment object

        Args:
                - trials: number of trials
                - filename: name for the recorded data
                - path: path for saving the recorded data (if not given it will be saved in current directory)
        """


        platform = pyglet.window.get_platform()
        display = platform.get_default_display()
        screen = display.get_screens()[screen_ind]
        super().__init__(screen=screen, *args, **kwargs)

        # create window

        self.arduino = arduino
        if not arduino:
            warn('Arduino not set for experiment.  Data will not be sent or received. To use, set the "device" in BaseExperiment')


        self.stim = stim

        # create Data object
        self.data = Data()

        self.trials = trials
        self.on_width = _gen_iter(on_width)
        self.off_width = _gen_iter(off_width)

    def end(self):
        self.close()  # exit the pyglet app
        if self.arduino:
            self.arduino.disconnect()  # close the serial communication channel

    @abstractmethod
    def run(self):
        """ runs the experiment in the passed application window"""
        pass


def _gen_iter(vals):
    if not hasattr(vals, '__iter__'):
        for val in cycle([vals]):
            yield val
    elif len(vals) == 2:
        while True:
            yield random.uniform(vals[0], vals[1])
    else:
        raise TypeError("'vals' must contain one or two values")


class DisplayExperiment(BaseExperiment):
    """ Experiment object to measure display latency measurement

    """
    def __init__(self, stim, *args, **kwargs):
        super(self.__class__, self).__init__(*args, stim=stim, **kwargs)

    def run(self):
        """ runs the experiment in the passed application window"""
        for trial in range(1, self.trials + 1):
            if self.arduino:
                self.arduino.init_next_trial()
            self.clear()
            self.stim.draw()
            self.flip()
            sleep(next(self.on_width))
            self.clear()
            self.flip()
            sleep(next(self.off_width))
            if self.arduino:
                dd = self.arduino.read()
                self.data.values.extend(dd)
        self.end()

class TrackingExperiment(BaseExperiment):
    """ Experiment object for tracking latency measurement

    """
    def run(self):
        """ runs the experiment in the passed application window"""

        for trial in range(1, self.trials+1):
            pass



class TotalExperiment(BaseExperiment):
    """ Experiment object for total latency measurement

    """
    def run(self):
        raise NotImplementedError
