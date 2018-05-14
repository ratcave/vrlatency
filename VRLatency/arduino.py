import serial
from struct import unpack


class Arduino(object):
    """ Handles attributes and methods related to stimulation/recording device

    Attributes:
        channel:
        is_connected (bool):

    """
    pkt_formats = {'Tracking': 'I2H', 'Display': 'I2H', 'Total': 'I2H'}
    pkt_size = {'Tracking': 8, 'Display': 8, 'Total': 8}
    n_point_options = {'Tracking': 240, 'Display': 240, 'Total': 240}

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
        """ Display a list of connected devices to the machine

        Returns:
            list of the ports and the connected devices to this machine

        """
        raise NotImplementedError()

    def disconnect(self):
        """Disconnect the device."""
        self.channel.close()

    @property
    def is_connected(self):
        return self.channel.isOpen()

    def read(self, n_points=240):
        return unpack('<' + self.packet_fmt * self.n_points, self.channel.read(self.packet_size * self.n_points))

    def init_next_trial(self):
        self.channel.write(bytes('S', 'utf-8'))

    def ping(self):
        """Returns True if Arduino is connected and has correct code loaded."""
        self.channel.readline()
        self.channel.write(bytes('are_you_ready?', 'utf-8'))
        packet = self.channel.read(30)
        response = unpack('<3c', packet)
        return True if response == 'yes' else False