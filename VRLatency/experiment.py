from __future__ import absolute_import

from abc import abstractmethod
import pyglet
from pyglet.window import key
import random
from warnings import warn
from time import sleep, time, perf_counter
from .data import Data
from itertools import cycle


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
        self.current_trial = 0
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
            self.current_trial += 1
            self.arduino.init_next_trial() if self.arduino else None
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
    while True:
        if not hasattr(vals, '__iter__'):
                yield vals
        elif len(vals) == 2:
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

    NOTE: in this experiment the timing information is recorded on Python side:
    === Start of trial
    1. Movement is sent to Arduino by python (communication time is insignificant)
    2. LEDs move on the VRLatency shield and at the same time the LED positions are being tracked
    3. Timing between the movement command and changes in position are compared and the tracking delay is characterize
    === End of trial
    """

    def __init__(self, rigid_body, *args, **kwargs):
        """ initialize a TrackigExperiment object

        Args:
                - rigid_body: is the object that has position attributes
        """
        super(self.__class__, self).__init__(*args, **kwargs)

        self.rigid_body = rigid_body
        self._pos = cycle(['L', 'R'])

    def run_trial(self):
        """ a single trial"""
        next_pos = next(self._pos)
        self.arduino.write(next_pos) if self.arduino else None
        start_time = perf_counter()
        while (perf_counter() - start_time) < .04:  # period of one trial
            t, led_pos = perf_counter(), -10 * self.rigid_body.position.x
            sleep(.001)  # to decrease the data point resolution to a millisecond
            self.data.values.append([start_time, t, led_pos, self.current_trial, 0 if next_pos == 'L' else 1])

        sleep(random.random() * .1 + .03)  # ITI (Inter-trial Interval) generated randomly

    #TODO: For the code on Arduino side add the start trial character

class TotalExperiment(BaseExperiment):
    """ Experiment object for total latency measurement

    NOTE: In this experiment the timing information is recorded by Arduino
    === start of the trial
    1. LED lights moves from one set of LEDs to another - timing info recorded
    2. LED movement is tracked and a new images is displayed (on top of the corresponding sensor) -> timing info recorded
    * the same process is repeated
    === end of the trial

    """

    def __init__(self, stim, rigid_body, *args, **kwargs):
        super(self.__class__, self).__init__(*args, stim=stim, **kwargs)

        self.rigid_body = rigid_body
        self.stim_with_tracking()

    def run_trial(self):
        """ a single trial"""
        self.data.values.append(self.arduino.read())

    def stim_with_tracking(self):

        @self.event
        def on_draw():
            self.clear()
            self.stim.draw()

        def update(dt):
            self.stim.position = -self.rigid_body.position.x * 1.6 - .39
            self.stim.position = self.rigid_body.position.z - .15

        pyglet.clock.schedule(update)
