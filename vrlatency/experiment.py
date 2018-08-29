from __future__ import absolute_import

from abc import abstractmethod
import pyglet
import random
from warnings import warn
from time import sleep, perf_counter
from datetime import datetime
from collections import OrderedDict
import csv
from tqdm import tqdm
import subprocess
from warnings import warn
import sys


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
                 on_width=.5, bckgrnd_color=(0, 0, 0), *args, **kwargs):
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

        self.experiment_type = 'Unknown'

        self.arduino = arduino
        if not arduino:
            warn('Arduino not set for experiment.  Data will not be sent or received.')

        self.bckgrnd_color = bckgrnd_color
        self.stim = stim
        if self.stim:
            self.stim.screen = screen
        self.data = []
        self.data_columns = []

        self.trials = trials
        self.current_trial = 0
        self.on_width = _gen_iter(on_width)
        self.off_width = _gen_iter(on_width[0]) if hasattr(on_width, '__iter__') else _gen_iter(on_width)

        self.params = OrderedDict()
        self.params['Experiment'] = self.__class__.__name__
        self.params['Date'] = datetime.now().strftime('%d.%m.%Y')
        self.params['Time'] = datetime.now().strftime('%H:%M:%S')
        disp_params = {key.title(): value for key, value in screen.get_mode().__dict__.items() if isinstance(value, int)}

        if sys.platform == 'win32':
            code = r"""
                 $Monitors = Get-WmiObject WmiMonitorID -Namespace root\wmi

                 ForEach ($Monitor in $Monitors){
                   $Manufacturer = ($Monitor.ManufacturerName -notmatch 0 | ForEach{[char]$_}) -join ""
                   $Name = ($Monitor.UserFriendlyName -notmatch 0 | ForEach{[char]$_}) -join ""
                   $Serial = ($Monitor.SerialNumberID -notmatch 0 | ForEach{[char]$_}) -join ""

                   echo "$Manufacturer,$Name,$Serial"
                 }
                 """
            proc = subprocess.Popen(['powershell', code], stdout=subprocess.PIPE)
            res = proc.communicate()[0].decode('utf8')
            disp_params['Monitors'] = ', '.join(res.replace(',', '_').splitlines())
        else:
            disp_params['Monitors'] = ' '
            warn("Monitor Name not detected; Feature only supported on Windows.")
        self.params.update(disp_params)

    def on_close(self):
        """Ends the experiment by closing the app window and disconnecting arduino"""
        self.arduino.disconnect() if self.arduino else None

    def run(self, remove_first_trial=True):
        """Runs the experiment"""
        for self.current_trial in tqdm(range(1, self.trials + 2), ascii=True):
            self.dispatch_events()
            self.arduino.init_next_trial() if self.arduino else None
            self.run_trial()

            if self.current_trial == 1 and remove_first_trial:
                self.data = []

        self.close()


    @abstractmethod
    def run_trial(self):
        """A single trial"""
        pass

    @property
    def bckgrnd_color(self):
        """Background color getter"""
        return self._bckgrnd_color

    @bckgrnd_color.setter
    def bckgrnd_color(self, value):
        """Background color setter"""
        self._bckgrnd_color = value
        pyglet.gl.glClearColor(value[0], value[1], value[2], 1)

    def save(self, filename=None):
        """ Save data into a csv file """

        if not filename:
            filename = '{}_{}.csv'.format(self.experiment_type.lower(), datetime.now().strftime('%Y%m%d_%H%M%S'))

        with open(filename, "w", newline='') as csv_file:
            header = ['{}: {}\n'.format(key, value) for key, value in self.params.items()]
            csv_file.writelines(header)
            csv_file.write("\n")

            writer = csv.writer(csv_file, delimiter=',')
            writer.writerow(self.data_columns)
            writer.writerows(self.data)


class DisplayExperiment(BaseExperiment):
    """Measures display latency"""

    def __init__(self, stim, *args, **kwargs):
        """ 
        """
        super(self.__class__, self).__init__(*args, stim=stim, **kwargs)
        self.experiment_type = 'Display'
        self.data_columns = ['Time', 'SensorBrightness', 'Trial']

    def run_trial(self):
        """A single trial"""
        self.clear()
        self.stim.draw()
        self.flip()
        sleep(next(self.on_width))
        self.clear()
        self.flip()
        sleep(next(self.off_width))
        self.data.extend(self.arduino.read()) if self.arduino else None


class TrackingExperiment(BaseExperiment):
    """Measures tracking latency

    NOTES: 
        In this experiment the timing information is recorded on Python side. 
        here is a description of a single trial:
        1. Movement is sent to Arduino by python (communication time is insignificant)
        2. LEDs move on the VRLatency shield and at the same time the LED positions are being tracked
        3. Timing between the movement command and changes in position are compared and the tracking delay is characterized
    """

    def __init__(self, rigid_body, on_width=.04, *args, **kwargs):
        """ Integrates all the needed elements for tracking latency measuremnt

        Arguments:
            - rigid_body (tracking obj): Tracking object that has position attributes
            - trial_period (float, optional): Period of a single trial
            - amplify_dist (float, optional): Amplification factor for stimulus distance, based on tracked object's position
            - *args, **kwargs: other arguments accepted by BaseExperiment class
        """
        super(self.__class__, self).__init__(*args, visible=False, **kwargs)
        self.rigid_body = rigid_body
        self.on_width = _gen_iter(on_width)
        self.experiment_type = 'Tracking'
        self.data_columns = ['Time', 'LED_Position', 'Trial']

    def run_trial(self):
        """A single trial"""
        start_time = perf_counter()
        next_trial_period = next(self.on_width)
        while (perf_counter() - start_time) < next_trial_period:
            t, led_pos = perf_counter(), self.rigid_body.position.z
            sleep(.001)  # to decrease the data point resolution to a millisecond
            self.data.append([t, led_pos, self.current_trial])


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

    def __init__(self, stim, rigid_body, stim_distance=.01, *args, **kwargs):
        """ Integrates all the needed elements for total latency measuremnt

        Arguments:
            - rigid_body (tracking obj): Tracking object that has position attributes
            - stim (Stimulus obj, optional): Stimulation object to be displayed by the display/projector
            - *args, **kwargs: other arguments accepted by BaseExperiment class
        """

        super(self.__class__, self).__init__(*args, stim=stim, **kwargs)
        self.rigid_body = rigid_body
        self.experiment_type = 'Total'
        self.data_columns = ['Time', 'LeftSensorBrightness', 'RightSensorBrightness', 'Trial', 'LED_State']

        self.stim_distance = stim_distance
        mean_rb_pos, n_checks = 0, 100
        for _ in tqdm(range(n_checks), ascii=True, desc="Finding the mean"):
            self.arduino.init_next_trial()
            sleep(.05)
            mean_rb_pos += self.rigid_body.position.z / float(n_checks)
            self.arduino.channel.read_all()  # empty the buffer (because Arduino is sending info anyway)
        self.mean_rb_pos = mean_rb_pos

    def run_trial(self):
        """ A single trial"""
        self.stim.position = self.stim_distance * (self.rigid_body.position.z - self.mean_rb_pos), 0
        self.clear()
        self.stim.draw()
        self.flip()
        sleep(next(self.on_width))
        self.data.extend(self.arduino.read()) if self.arduino else None


def _gen_iter(vals):
    """ Generator function for on and off width given one or two values"""
    while True:
        if not hasattr(vals, '__iter__'):
            yield vals
        elif len(vals) == 2:
            yield random.uniform(vals[0], vals[1])
        else:
            raise TypeError("values passed as on_width and off_width must contain one or two values")
