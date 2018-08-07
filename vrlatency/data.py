import csv
import numpy as np


class Data(object):
    """ Data object handling data-related matters

    Attributes:
        values: stores the recorded data during the experiment (if record is set to True, and there exist a recording device)
    """

    def __init__(self):
        self.values = []

    def extend(self, value):
        self.values.extend(value)

    def __write_data(self, file_obj, data, fieldnames):
        writer = csv.DictWriter(file_obj, delimiter=',', fieldnames=fieldnames)
        writer.writeheader()

        list_of_dicts = []
        for values in data:
            inner_dict = dict(zip(fieldnames, values))
            list_of_dicts.append(inner_dict)

        for dicts in list_of_dicts:
            writer.writerow(dicts)

    def to_csv(self, path, experiment_params=None, columns=None):
        """ Save data into a csv file """

        # write the experiment parameters (header)
        with open(path, "w", newline='') as csv_file:
            header = ['{}: {}\n'.format(key, value) for key, value in experiment_params.items()]
            csv_file.writelines(header)
            csv_file.writelines("\n")

            # reshape the data
            data = [self.values[i:i+len(columns)] for i in range(0, len(self.values), len(columns))]

            # check if columns are empty use integer index
            self.__write_data(csv_file, data, columns)

    @staticmethod
    def from_csv(path):
        """reads the data from csv file"""

        # TODO: user should be able to give the column labels as an input

        with open(path, "r") as f:
            dd = f.readlines()

        dd = dd[dd.index('\n')+1:]
        dd = [el[:-1] for el in dd]
        columns = dd[0].split(',')
        data = [el.split(',') for el in dd[1:]]
        data = list(zip(*data))
        data = {cc:list(map(int, dd)) for cc, dd in zip(columns, data)}

        return data

    @staticmethod
    def __rolling(data, window_size, set_to='center', stride=1):
        """applies a rectangular window on data for the purpose of smoothing"""
        data_rolled = np.zeros(data.shape)
        for i in range(0, data.shape[0] - window_size + 1, stride):
            window_data = data[i:i+window_size]
            if set_to == 'right':
                data_rolled[i+window_size-1] = window_data.max()
            elif set_to == 'left':
                data_rolled[i] = window_data.max()
            else:
                data_rolled[i+window_size//2] = window_data.max()

        return data_rolled

    def get_latency(self, experiment_type, shape, effect_index, trial_index=None, effect_time_index=None, trial_time_index=None):
        """ Displays the histogram of the latency measured in each trial

        NOTE:
            Usually we have the trial number and its timing, which marks the beginning of the trial.
            We also have the timing information where we are expecting the effect (sensor information).
            The difference of these two timing information in each trial gives us the delay in each trial.
            This latency values are returned. This function also ignores the first trial  latency value.
        """

        effect_time_index = 0 if not effect_time_index else effect_time_index
        trial_time_index = 0 if not trial_time_index else trial_time_index
        trial_index = -1 if not trial_index else trial_index

        # shape the data in the right way
        dd = np.array(self.values).reshape(shape)
        dd = dd.astype(float)

        # change the timing information depending on the experiment_type (this depends on which side is handling time):
        # Display -> Arduino -> microseconds
        # Tracking -> Python -> seconds (with microsecond resolution)
        # Total -> Arduino -> microseconds
        # and we want all the timing information to be in millisecond
        time_mult = 1000 if experiment_type == 'Tracking' else .001
        dd[:, trial_time_index] = dd[:, trial_time_index] * time_mult
        if effect_time_index != trial_time_index:
            dd[:, effect_time_index] = dd[:, effect_time_index] * time_mult

        # get the time of the start of a trial (a row/column vector)
        trial_start = np.diff(dd[:, trial_index])
        trial_start = np.insert(trial_start, 0, 0)
        trial_start_time = dd[trial_start == 1, trial_time_index]
        trial_start_time = np.insert(trial_start_time, 0, dd[0, trial_time_index])  # adding the first trial starting time

        # get the timing of when the effect was sensed (a row/column vector)
        # smoothing the data (a binary signal)
        dd_smooth = np.zeros(dd[:, effect_index].shape)
        dd_smooth[dd[:, effect_index] >= dd[:, effect_index].mean()] = 1

        # apply a rolling window (sets the  values to the value of right edge)
        dd_smooth = self.__rolling(dd_smooth, window_size=10, set_to='right')
        effect_start = np.diff(dd_smooth)
        effect_start = np.insert(effect_start, 0, 0)
        effect_start = effect_start if experiment_type == 'Display' else np.abs(effect_start)
        effect_start_time = dd[effect_start == 1, effect_time_index]

        # get the latency values (difference between trial and effect)
        latencies = effect_start_time - trial_start_time

        return latencies[1:]  # ignore the first value
