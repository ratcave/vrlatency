import vrlatency as vrl


def test_ping():
    arduino = vrl.Arduino(port='COM9', baudrate=250000, experiment_type='Total')
    assert arduino.ping
