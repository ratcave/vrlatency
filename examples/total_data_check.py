import vrlatency as vrl
import natnetclient as natnet
import numpy as np

myarduino = vrl.Arduino(port='COM9', baudrate=250000, experiment_type='Total')

# create a stimulation pattern
mystim = vrl.Stimulus(position=(0, 0), color=(0, 0, 0))
mystim.mesh.point_size = 5
mystim.mesh.scale.xyz = .03, .2, 1

# specify the object that is being tracked
client = natnet.NatClient()
led = client.rigid_bodies['LED']

# create an experiment app
myexp = vrl.TotalExperiment(#arduino=myarduino,
                            stim=mystim,
                            rigid_body=led,
                            trials=1000,
                            screen_ind=1,
                            fullscreen=True)
myexp.run()

# get the data
dd = np.array(myexp.data.values).reshape(-1, 5)
