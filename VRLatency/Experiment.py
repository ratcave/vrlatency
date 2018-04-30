import pyglet
import serial
import numpy as np
import pandas as pd
import ratcave as rc
from struct import unpack

def connect_to_arduino(port=None, baudrate=None):
    """Connect to Arduino board

    Input:
            - port
            - baudrate

    returns:

    """
    if (port is None) or (baudrate is None):
        raise ValueError("Specify both port and baudrate for the communication channel.")

    ARDUINO_PORT = port
    BAUDRATE = baudrate
    print('Connecting...')
    device = serial.Serial(ARDUINO_PORT, baudrate=BAUDRATE, timeout=2.)
    device.readline()
    print('Connection successful!')


class Experiment(object):

    def __init__(self, trials=20, filename=None, path=None):
        """ Initialize an experiment object

        Inputs:
                - trials: number of trials
                - filename: name for the recorded data
                - path: path for saving the recorded data (if not given it will be saved in current directory)


        """

        # Checking the necessary inputs
        if filename is None:
            raise ValueError("Specify a name for the recorded data")


    def add_mesh(self):
        pass

    def _save_data(self, data, filename, path):
        dd = np.array(data).reshape(-1, 3)
        df = pd.DataFrame(data=dd, columns=['Time', "Chan1", 'Trial'])
        df.to_csv('../Measurements/' + filename + '.csv', index=False)

    def run(self):
        """ runs the experiment in the passed application window

        Input:
                - window

        return:

        """
        pass
