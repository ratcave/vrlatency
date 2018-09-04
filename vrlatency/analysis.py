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



def perc_range(x, perc):
    return perc * np.ptp(x) + np.min(x)


def get_display_latencies(df, thresh=.75):
    latencies = []
    ntrials = df.Trial.max()
    sensorf, timef, trialf = df[['SensorBrightness', 'Time', 'Trial']].values.T
    threshf = perc_range(sensorf, thresh)
    for trial in range(2, ntrials):
        is_trial = trialf == trial
        sensor = sensorf[is_trial]
        time = timef[is_trial]
        off_idx = np.where(sensor < threshf)[0][0]

        try:
            detect_idx = np.where(sensor[off_idx:] > threshf)[0][0]
            latency = time[detect_idx + off_idx] - time[0]
            latencies.append(latency)
        except IndexError:
            latencies.append(np.nan)

    return pd.Series(data=latencies, name='DisplayLatency')



def get_tracking_latencies(df):
    """ Returns the latency values for each trial of a Tracking Experiment"""
    def detect_latency(df, thresh):
        diff = np.diff(df.RigidBody_Position > thresh)
        idx = np.where(diff != 0)[0][0]
        return df.Time.iloc[idx] - df.Time.iloc[0]

    latencies = df.groupby('Trial').apply(detect_latency, thresh=df.RigidBody_Position.mean())
    latencies.name = 'TrackingLatency'
    return latencies


def get_total_latencies(df):
    """ Returns the latency values for each trial of a Total Experiment"""

    data = df.copy()

    # Make columns with Sensor/LED values used for each trial
    sensors = {False: 'LeftSensorBrightness', True: 'RightSensorBrightness'}
    data['Sensor'] = data.apply(lambda row: row[sensors[row['LED_State']]], axis=1)

    thresh = data[['LeftSensorBrightness', 'RightSensorBrightness']].values.mean()

    # Apply trial-based time series analysis
    trials = data.groupby('Trial')
    latencies = trials.apply(lambda df: (df.Time.iloc[[np.where(df.Sensor > thresh)[0][0]]] - df.Time.iloc[0]).values[0])
    latencies.name = 'Total Trial Latency (us)'

    # Return dataframe of latencies (Trials x (Group, Latency)
    return latencies



