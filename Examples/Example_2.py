import VRLatency as vrl

# connect to device
arduino = vrl.Device(port='COM9', baudrate=250000)

# create a window
mywin = vrl.Window(screen_ind=1, fullscreen=True)

# create a stimulus
mystim = vrl.Stim(position=(0, 0))

# create an experiment app
myexp = vrl.DisplayExperiment(window=mywin, stim=mystim, device=arduino)

# run the experiment
myexp.run(on_width=.5, off_width=[.2, .5])