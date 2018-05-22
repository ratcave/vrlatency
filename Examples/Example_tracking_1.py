import vrlatency as vrl
import natnetclient as natnet

# connect to the device
arduino = vrl.Arduino(experiment_type='Tracking', port='COM9', baudrate=250000)

# specify the object that is being tracked
client = natnet.NatClient()
LED = client.rigid_bodies['LED']

# create an experiment app
myexp = vrl.TrackingExperiment(arduino=arduino,
                               rigid_body=LED,
                               trials=1000)

myexp.run()