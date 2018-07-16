import vrlatency as vrl
import numpy as np
import matplotlib.pyplot as plt

# specify and connect to device
# myarduino = vrl.Arduino(port='COM9', baudrate=250000, experiment_type='Display')

myarduino = vrl.Arduino.from_experiment_type(experiment_type='Display', port='COM9', baudrate=250000)

# create a stimulus
mystim = vrl.Stimulus(position=(0, 0), color=(1, 1, 1))
mystim.mesh.point_size = 5
mystim.mesh.scale.xyz = .0225, .2, 1

# create an experiment
myexp = vrl.DisplayExperiment(arduino=myarduino,
                              trials=50,
                              fullscreen=True, screen_ind=1,
                              stim=mystim,
                              on_width=0,
                              off_width=.02)  #[0, .3])

myexp.run()

# get the data
dd = np.array(myexp.data.values).reshape(-1, 3)

plt.plot(dd[:, 0]/1000000, dd[:, 1])
plt.show()
