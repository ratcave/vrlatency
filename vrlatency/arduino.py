import serial
import serial.tools.list_ports
from struct import unpack


class Arduino(object):
    """ Handles attributes and methods related to stimulation/recording device

    Attributes:
        - port:
        - baudrate:
        - packet_fmt:
        - packet_size:
        - n_points:
        - channel:
    """
    options = {'Display': dict(packet_fmt='I2H', packet_size=8, n_points=500),
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
        """ Displays the connected arduino devices to the machine"""
        ports = list(serial.tools.list_ports.comports())
        for p in ports:
            if ('Arduino' or 'arduino') in str(p):
                print(p)

    def disconnect(self):
        """Disconnect the device"""
        self.channel.close()

    @property
    def is_connected(self):
        "Returns True if arduino is connected, and False otherwise."
        return self.channel.isOpen()

    def read(self):
        """Reads data packets sent over serial channel by arduino

        Returns:
            - list: data recorded by arduino
        """
        return unpack('<' + self.packet_fmt * self.n_points, self.channel.read(self.packet_size * self.n_points))

    def write(self, msg):
        """Write to arduino over serial channel

        Arguments:
            - msg (str): message to be sent to arduino
        """
        self.channel.write(bytes(msg, 'utf-8'))

    def init_next_trial(self):
        """Sends a message to arduino to signal start of a trial"""
        self.write('S')

    # TODO: Add pinging to Arduino code (added to total, but not others!)
    def ping(self):
        """Checks connection.

        Returns:
            - bool: True if arduino is connected, False otherwise
        """
        self.channel.readline()
        self.channel.write(bytes('R', 'utf-8'))
        packet = self.channel.read(10)
        response = packet.decode(encoding='utf-8')
        return True if response == 'yes' else False
