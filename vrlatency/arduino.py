import serial
import serial.tools.list_ports
from struct import unpack


class Arduino(object):
    """ Handles attributes and methods related to stimulation/recording device

    Attributes:
        channel:
        is_connected (bool):

    """
    options = {'Display': dict(packet_fmt='I2H', packet_size=8, n_points=100),
               'Total': dict(packet_fmt='I3H?', packet_size=11, n_points=500),
               'Tracking': dict(packet_fmt='-', packet_size=0, n_points=0),
               }

    def __init__(self, port, baudrate, packet_fmt, packet_size, n_points):
        """
        Interfaces and Connects to an arduino running the VRLatency programs.

        Arguments:
            - port (str): The port the arduino is conected on (ex: 'COM8')
            - baudrate (int): The baud rate for the arduino connection.
        """
        self.port = port
        self.baudrate = baudrate
        self.packet_fmt = packet_fmt
        self.packet_size = packet_size
        self.n_points = n_points
        self.channel = serial.Serial(self.port, baudrate=self.baudrate, timeout=2.)
        self.channel.readline()

    @classmethod
    def from_experiment_type(cls, experiment_type, *args, **kwargs):
        """Auto-gen Arduino params from experiment_type ('Tracking', 'Display', or 'Total')"""
        options = cls.options[experiment_type].copy()
        options.update(kwargs)
        return cls(*args, **options)

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

    # TODO: Add pinging to Arduino code (added to total, but not others!)
    def ping(self):
        """Returns True if Arduino is connected and has correct code loaded."""
        self.channel.readline()
        self.channel.write(bytes('R', 'utf-8'))
        packet = self.channel.read(10)
        response = packet.decode(encoding='utf-8')
        return True if response == 'yes' else False
