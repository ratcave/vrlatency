import vrlatency as vrl
import numpy as np
import matplotlib.pyplot as plt

# specify and connect to device
myarduino = vrl.Arduino(port='COM9', baudrate=250000, experiment_type='Display')

# create a stimulus
mystim = vrl.Stimulus(position=(0, 0), color=(1, 1, 1))
mystim.mesh.point_size = 5
mystim.mesh.scale.xyz = .03, .2, 1

# create an experiment
myexp = vrl.DisplayExperiment(arduino=myarduino,
                              trials=100,
                              fullscreen=True, screen_ind=1,
                              stim=mystim,
                              on_width=.05,
                              off_width=[0, .3])

myexp.run()

# get the data
dd = np.array(myexp.data.values).reshape(-1, 3)
