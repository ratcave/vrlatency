import VRLatency as vrl

# connect to the device
arduino = vrl.Arduino(experiment_type='Display', port='COM9', baudrate=250000)

# create a stimulation pattern
mystim = vrl.Stim(position=(0, 0))

# create an experiment app
myexp = vrl.DisplayExperiment(arduino=arduino,
                              stim=mystim, on_width=0.5, off_width=[0.1, .4])
myexp.run()