import vrlatency as vrl
import natnetclient as natnet
import numpy as np


# connect to device
myarduino = vrl.Arduino.from_experiment_type(experiment_type='Total', port='COM9', baudrate=250000)

# create a stimulation pattern
mystim = vrl.Stimulus(position=(0, 0), color=(1, 1, 1), size=5)
mystim.mesh.scale.xyz = .022, .2, 1

# specify the object that is being tracked
client = natnet.NatClient()
led = client.rigid_bodies['LED']

# create an experiment app
myexp = vrl.TotalExperiment(arduino=myarduino,
                            stim=mystim,
                            on_width=[.1, .3],
                            rigid_body=led,
                            trials=100,
                            screen_ind=1,
                            fullscreen=True)
myexp.run()

# get the data
dd = np.array(myexp.data.values).reshape(-1, 5)
