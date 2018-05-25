from vrlatency import *

# set the arduino connection
arduino = Arduino(port='COM9', baudrate=250000, experiment_type='Display')

# specify the stimulus
stim = Stimulus(position=(0, 0), color=(1., 0., 0.))

# we have the device, we have the stimulus, we need an experiment to run!
exp = DisplayExperiment(screen_ind=1, fullscreen=True,
                        arduino=arduino, stim=stim,
                        on_width=.2, off_width=[.1, .3], trials=100,
                        bckgrnd_color=(.8, .8, .8))

exp.run()