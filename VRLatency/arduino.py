import serial
import serial.tools.list_ports
from struct import unpack


class Arduino(object):
    """ Handles attributes and methods related to stimulation/recording device

    Attributes:
        channel:
        is_connected (bool):

    """
    pkt_formats = {'Tracking': '-', 'Display': 'I2H', 'Total': 'I3H?'}
    pkt_size = {'Tracking': 0, 'Display': 8, 'Total': 11}
    n_point_options = {'Tracking': 0, 'Display': 100, 'Total': 500}

    def __init__(self, experiment_type, port, baudrate):
        """Can be 'Tracking', 'Display', or 'Total'"""
        self.port = port
        self.baudrate = baudrate
        self.channel = serial.Serial(self.port, baudrate=self.baudrate, timeout=2.)
        self.experiment_type = experiment_type
        self.packet_fmt = self.pkt_formats[experiment_type]
        self.packet_size = self.pkt_size[experiment_type]
        self.n_points = self.n_point_options[experiment_type]
        self.channel.readline()

    @staticmethod
    def find_all():
        """ Display a list of connected devices to the machine"""

        ports = list(serial.tools.list_ports.comports())
        for p in ports:
            if ('Arduino' or 'arduino') in str(p):
                print(p)

    def disconnect(self):
        """Disconnect the device"""
        self.channel.close()

    @property
    def is_connected(self):
        return self.channel.isOpen()

    def read(self):
        return unpack('<' + self.packet_fmt * self.n_points, self.channel.read(self.packet_size * self.n_points))

    def write(self, msg):
        self.channel.write(bytes(msg, 'utf-8'))

    def init_next_trial(self):
        self.write('S')

    # TODO: Add pinging to Arduino code
    def ping(self):
        """Returns True if Arduino is connected and has correct code loaded."""
        self.channel.readline()
        self.channel.write(bytes('are_you_ready?', 'utf-8'))
        packet = self.channel.read(30)
        response = unpack('<3c', packet)
        return True if response == 'yes' else False