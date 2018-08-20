import numpy as np
import pandas as pd
from io import StringIO


def read_params(path):
    """ Returns the parameters of experiment data file"""
    with open(path, "r") as f:
        header, body = f.read().split('\n\n')
    return dict([param.split(': ') for param in header.split('\n')])


def read_csv(path):
    """ Returns the data of experiment data file"""
    with open(path, "r") as f:
        header, body = f.read().split('\n\n')
    return pd.read_csv(StringIO(body))


def get_display_latencies(df):
    """ Returns the latency values for each trial of a Display Experiment"""
    def detect_latency(df, thresh):
        idx = np.where(df.SensorBrightness > thresh)[0][0]
        return df.Time.iloc[idx] - df.Time.iloc[0]

    latencies = df.groupby('Trial').apply(detect_latency, thresh=df.SensorBrightness.mean())
    latencies.name = 'DisplayLatency'
    return latencies


def get_tracking_latencies(df):
    """ Returns the latency values for each trial of a Tracking Experiment"""
    def detect_latency(df, thresh):
        diff = np.diff(df.LED_Position > thresh)
        idx = np.where(diff != 0)[0][0]
        return df.Time.iloc[idx] - df.Time.iloc[0]

    latencies = df.groupby('Trial').apply(detect_latency, thresh=df.LED_Position.mean())
    latencies.name = 'TrackingLatency'
    return latencies


def get_total_latencies(df):
    """ Returns the latency values for each trial of a Total Experiment"""
    df = df.copy()
    df['SensorDiff'] = df.LeftSensorBrightness - df.RightSensorBrightness

    import ipdb
    ipdb.set_trace()

    def detect_latency(df, thresh):
        diff = np.diff(df.SensorDiff > thresh)
        idx = np.where(diff != 0)[0][0]
        return df.Time.iloc[idx] - df.Time.iloc[0]

    latencies = df.groupby('Trial').apply(detect_latency, thresh=df.SensorDiff.mean())
    latencies.name = 'TotalLatency'
    return latencies
