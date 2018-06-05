import vrlatency as vrl


def test_ping():
    arduino = vrl.Arduino.from_experiment_type('Total', port='COM9', baudrate=250000)
    assert arduino.ping


def test_overridable():
    arduino = vrl.Arduino.from_experiment_type('Total', port='COM9', baudrate=250000, packet_size=2)
    assert arduino.packet_size == 2
