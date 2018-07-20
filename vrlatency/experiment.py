from __future__ import absolute_import

from abc import abstractmethod
import pyglet
from pyglet.window import key
import random
from warnings import warn
from time import sleep, perf_counter
from .data import Data


class BaseExperiment(pyglet.window.Window):
    """Experiment abstract base method

    Attributes:
        - arduino:
        - bckgrnd_color:
        - stim:
        - data:
        - trials:
        - current_trial:
        - on_width:
        - off_width:
    """

    def __init__(self, arduino=None, screen_ind=0, trials=20, stim=None,
                 on_width=.5, off_width=.5, bckgrnd_color=(0, 0, 0), *args, **kwargs):
        """Integrates other components and let's use to run, record and store experiment data

        Arguments:
            - arduino (Arduino obj, optional): Arduino object used for recording and/or movement simulation
            - screen_ind (int, optional): Specifies the screen in which the window app will be displayes
            - trials (int, optional): Number of trials
            - stim (Stimulation obj, optional): Stimulation object to be displayed by the display/projector
            - on_width (float, optional): Time period for the stimulus to be visible
            - off_width (float, optional): Time period for the stimulus to be invisible
            - bckgrnd_color (float, optional): Backgorund color of experiment window app
            - *args, **kwargs: other arguments of pyglet Window class
        """

        platform = pyglet.window.get_platform()
        display = platform.get_default_display()
        screen = display.get_screens()[screen_ind]
        super().__init__(screen=screen, *args, **kwargs)

        self.arduino = arduino
        if not arduino:
            warn('Arduino not set for experiment.  Data will not be sent or received. To use, set the "device" in BaseExperiment')

        self.bckgrnd_color = bckgrnd_color
        self.stim = stim
        self.data = Data()

        self.trials = trials
        self.current_trial = 0
        self.on_width = _gen_iter(on_width)
        self.off_width = _gen_iter(off_width)

    def end(self):
        """Ends the experiment by closing the app window and disconnecting arduino"""
        self.close()
        self.arduino.disconnect() if self.arduino else None

    def run(self):
        """Runs the experiment"""
        for trial in range(1, self.trials + 1):
            # while not mywin.has_exit:
            self.dispatch_events()
            self.current_trial += 1
            self.arduino.init_next_trial() if self.arduino else None
            self.run_trial()
        self.end()

    @abstractmethod
    def run_trial(self):
        """A single trial"""
        pass

    def on_key_press(self, symbol, modifiers):
        """ Key press event for SPACE key"""
        if key.ESCAPE == symbol:
            self.end()

    @property
    def bckgrnd_color(self):
        """Background color getter"""
        return self._bckgrnd_color

    @bckgrnd_color.setter
    def bckgrnd_color(self, value):
        """Background color setter"""
        self._bckgrnd_color = value
        pyglet.gl.glClearColor(value[0], value[1], value[2], 1)


class DisplayExperiment(BaseExperiment):
    """Measures display latency"""

    def __init__(self, stim, *args, **kwargs):
        """ 
        """
        super(self.__class__, self).__init__(*args, stim=stim, **kwargs)

    def run_trial(self):
        """A single trial"""
        self.clear()
        self.stim.draw()
        self.flip()
        sleep(next(self.on_width))
        self.clear()
        self.flip()
        sleep(next(self.off_width))
        self.data.values.extend(self.arduino.read()) if self.arduino else None


class TrackingExperiment(BaseExperiment):
    """Measures tracking latency

    NOTES: 
        In this experiment the timing information is recorded on Python side. 
        here is a description of a single trial:
        1. Movement is sent to Arduino by python (communication time is insignificant)
        2. LEDs move on the VRLatency shield and at the same time the LED positions are being tracked
        3. Timing between the movement command and changes in position are compared and the tracking delay is characterized
    """

    def __init__(self, rigid_body, trial_period=.04, amplify_dist=-10, *args, **kwargs):
        """ Integrates all the needed elements for tracking latency measuremnt

        Arguments:
            - rigid_body (tracking obj): Tracking object that has position attributes
            - trial_period (float, optional): Period of a single trial
            - amplify_dist (float, optional): Amplification factor for stimulus distance, based on tracked object's position
            - *args, **kwargs: other arguments accepted by BaseExperiment class
        """
        super(self.__class__, self).__init__(*args, visible=False, **kwargs)
        self.rigid_body = rigid_body
        self.trial_period = trial_period
        self.amplify_dist = amplify_dist

    def run_trial(self):
        """A single trial"""
        start_time = perf_counter()
        while (perf_counter() - start_time) < self.trial_period:
            t, led_pos = perf_counter(), self.amplify_dist * self.rigid_body.position.x
            sleep(.001)  # to decrease the data point resolution to a millisecond
            self.data.extend([start_time, t, led_pos, self.current_trial])

        sleep(random.random() * .1 + .03)  # ITI (Inter-trial Interval) generated randomly


class TotalExperiment(BaseExperiment):
    """Experiment object for total latency measurement

    NOTES: 
        In this experiment the timing information is recorded by Arduino
        Here is a description of a single trial:
        1. LED lights moves from one set of LEDs to another - timing info recorded
        2. LED movement is tracked and a new images is displayed (on top of the corresponding sensor) -> timing info recorded
        * the same process is repeated

        By comparing the timing between the LED_state and the photodiode data the delay can be characterized
    """

    def __init__(self, stim, rigid_body, *args, **kwargs):
        """ Integrates all the needed elements for total latency measuremnt

        Arguments:
            - rigid_body (tracking obj): Tracking object that has position attributes
            - stim (Stimulus obj, optional): Stimulation object to be displayed by the display/projector
            - *args, **kwargs: other arguments accepted by BaseExperiment class
        """

        super(self.__class__, self).__init__(*args, stim=stim, **kwargs)
        self.rigid_body = rigid_body

    def run_trial(self):
        """A single trial"""
        self.stim.position = -(self.rigid_body.position.x + .564) * 100, 0
        self.clear()
        self.stim.draw()
        self.flip()
        sleep(next(self.on_width))
        self.data.values.extend(self.arduino.read()) if self.arduino else None


def _gen_iter(vals):
    """Generator function for on and off width given one or two values"""
    while True:
        if not hasattr(vals, '__iter__'):
            yield vals
        elif len(vals) == 2:
            yield random.uniform(vals[0], vals[1])
        else:
            raise TypeError("values passed as on_width and off_width must contain one or two values")
