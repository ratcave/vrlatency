import vrlatency as vrl
import random
import natnetclient as natnet


def test_total_tracking():
    myarduino = vrl.Arduino.from_experiment_type(port='COM9', baudrate=250000, experiment_type='Total')
    mystim = vrl.Stimulus(position=(0, 0), color=(1, 1, 1))
    mystim.mesh.point_size = 5
    mystim.mesh.scale.xyz = .03, .2, 1
    client = natnet.NatClient()
    led = client.rigid_bodies['LED']
    trials = random.randint(5, 16)
    myexp = vrl.TotalExperiment(arduino=myarduino,
                                stim=mystim,
                                on_width=[.01, .3],
                                rigid_body=led,
                                trials=trials,
                                screen_ind=1,
                                fullscreen=True)
    myexp.run()
    assert trials == myexp.data.values[-2]
    assert len(myexp.data.values) == 5 * 500 * trials  # each trial, 500 packets, each packet 5 elements
