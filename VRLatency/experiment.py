from __future__ import absolute_import

from abc import abstractmethod
import pyglet
from pyglet.window import key
import random
from itertools import cycle
from warnings import warn
from time import sleep
from .data import Data


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

    def run(self):
        """ runs the experiment in the passed application window"""
        for trial in range(1, self.trials + 1):
            self.dispatch_events()
            if self.arduino:
                self.arduino.init_next_trial()
            self.run_trial()
            if self.arduino:
                dd = self.arduino.read()
                self.data.values.extend(dd)
        self.end()

    @abstractmethod
    def run_trial(self):
        pass

    def on_key_press(self, symbol, modifiers):
        if key.ESCAPE == symbol:
            self.end()

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

    def run_trial(self):
        """ a single trial"""
        self.clear()
        self.stim.draw()
        self.flip()
        sleep(next(self.on_width))
        self.clear()
        self.flip()
        sleep(next(self.off_width))


class TrackingExperiment(BaseExperiment):
    """ Experiment object for tracking latency measurement

    """
    def run_trial(self):
        """ a single trial"""
        raise NotImplementedError


class TotalExperiment(BaseExperiment):
    """ Experiment object for total latency measurement

    """
    def run_trial(self):
        """ a single trial"""
        raise NotImplementedError
