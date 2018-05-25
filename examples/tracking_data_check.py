import vrlatency as vrl
import natnetclient as natnet
import numpy as np

# connect to device
myarduino = vrl.Arduino(port='COM9', baudrate=250000, experiment_type='Tracking')

# specify the object that is being tracked
client = natnet.NatClient()
led = client.rigid_bodies['LED']

myexp = vrl.TrackingExperiment(arduino=myarduino,
                               rigid_body=led,
                               trials=100)

myexp.run()

# get the data
dd = np.array(myexp.data.values).reshape(-1, 5)
