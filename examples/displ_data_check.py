import vrlatency as vrl

# specify and connect to device
myarduino = vrl.Arduino(port='COM9', baudrate=250000, experiment_type='Display')

# create a stimulus
mystim = vrl.Stimulus(position=(0, 0), color=(1, 1, 1))
mystim.mesh.point_size = 10
mystim.mesh.scale.xyz = .03, .2, 1

# create an experiment
myexp = vrl.DisplayExperiment(arduino=myarduino,
                              trials=100,
                              fullscreen=True, screen_ind=1,
                              stim=mystim,
                              on_width=.2,
                              off_width=[.1, .3])

myexp.run()