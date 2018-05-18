from VRLatency.experiment import BaseExperiment
import VRLatency as vrl

from time import sleep


class CustomExperiment(BaseExperiment):
    """ display something on the screen and send a command to arduino"""

    def __init__(self, stim, *args, **kwargs):
        super(self.__class__, self).__init__(*args, stim=stim, **kwargs)

        self.position = [(-.5, 0),
                         (-.25, 0),
                         (0, 0),
                         (.25, 0),
                         (.5, 0)]
        self.color = [(1, 0, 0),
                      (0, 1, 0),
                      (0, 0, 1),
                      (1, 1, 0),
                      (0, 1, 1)]

    def run_trial(self):
        """ a single trial"""

        print("trial number:", self.current_trial, self.bckgrnd_color)

        self.clear()
        for pos, col in zip(self.position, self.color):
            self.stim.position = pos
            self.stim.color = col
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
    myexp = CustomExperiment(  # arduino=arduino,
        stim=mystim, bckgrnd_color=(.3, .3, .3))
    myexp.run()


if __name__ == "__main__":
    main()
