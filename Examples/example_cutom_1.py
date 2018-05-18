from VRLatency.experiment import BaseExperiment
import VRLatency as vrl

from time import sleep

class CustomExperiment(BaseExperiment):
    """ display something on the screen and send a command to arduino"""
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
        self.data.values.append(self.arduino.read()) if self.arduino else None


def main():
    # connect to the device
    # arduino = vrl.Arduino(experiment_type='Display', port='COM9', baudrate=250000)

    # create a stimulation pattern
    mystim = vrl.Stimulus(position=(0, 0))

    # create an experiment app
    myexp = CustomExperiment(#arduino=arduino,
                             stim=mystim, on_width=.2, off_width=[.05, .2])
    myexp.run()


if __name__ == "__main__":
    main()

