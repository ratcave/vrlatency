import vrlatency as vrl

# connect to device
arduino = vrl.Arduino()
arduino.connect(port='COM9', baudrate=250000)

# create a window
mywin = vrl.Window(screen_ind=1, fullscreen=True)

# create a stimulus
mystim = vrl.Stimulus()
mystim.mesh.position.xyz = 0, 0, -3

# create an experiment app
myexp = vrl.DisplayExperiment(window=mywin, stim=mystim, device=arduino)

# run the experiment
myexp.run()