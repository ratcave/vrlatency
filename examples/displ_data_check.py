import vrlatency as vrl

# specify and connect to device
myarduino = vrl.Arduino(port='COM9', baudrate=250000, experiment_type='Display')

# create a stimulus
mystim = vrl.Stimulus(position=(.8, 0), color=(1, 0, 0))
mystim.mesh.scale.y = .2
# mystim.mesh.scale.y = .2
# mystim.mesh.scale.xyz = .2, .2, 1

# create an experiment
myexp = vrl.DisplayExperiment(arduino=myarduino,
                              trials= 100,
                              fullscreen=True, screen_ind=1,
                              stim=mystim,
                              on_width=.2,
                              off_width=[.1, .3])

myexp.run()