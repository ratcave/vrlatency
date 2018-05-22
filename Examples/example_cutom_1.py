from VRLatency.experiment import BaseExperiment
import VRLatency as vrl

from time import sleep
from itertools import cycle

class CustomExperiment(BaseExperiment):
    """ display something on the screen and send a command to arduino"""
    def __init__(self, stim, *args, **kwargs):
        super(self.__class__, self).__init__(*args, stim=stim, **kwargs)

        self.pos = cycle([-.5, .5])
        self.color = cycle([(1, 0, 0), (0, 0, 1)])

    def run_trial(self):
        """ a single trial"""
        self.stim.position = next(self.pos), 0
        self.stim.color = next(self.color)
        self.clear()
        self.stim.draw()
        self.flip()
        sleep(.5)
        self.data.values.append(self.arduino.read()) if self.arduino else None


def main():
    # connect to the device
    # arduino = vrl.Arduino(experiment_type='Display', port='COM9', baudrate=250000)

    # create a stimulation pattern
    mystim = vrl.Stimulus(position=(0, 0))

    # create an experiment app
    myexp = CustomExperiment(#arduino=arduino,
                             stim=mystim, bckgrnd_color=(.2, .5, .2))
    myexp.run()


if __name__ == "__main__":
    main()

