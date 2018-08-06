import csv
import numpy as np
import seaborn as sns


class Data(object):
    """ Data object handling data-related matters

    Attributes:
        values: stores the recorded data during the experiment (if record is set to True, and there exist a recording device)
    """

    def __init__(self):
        self.values = []

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
        with open(path, "w") as csv_file:
            header = ['{}: {}\n'.format(key, value) for key, value in experiment_params.items()]
            csv_file.writelines(header)
            csv_file.writelines("\n")

            # reshape the data
            data = [self.values[i:i+len(columns)] for i in range(0, len(self.values), len(columns))]

            # check if columns are empty use integer index
            self.__write_data(csv_file, data, columns)

    def from_csv(self, path):
        raise NotImplementedError

    def make_smooth(self):
        raise NotImplementedError

    def __rolling(self):
        raise NotImplementedError

    def get_hist(self, shape, effect_index, time_index=None, trial_index=None):
        """ Displays the histogram of the latency measured in each trial

        NOTE:
            Usually we have the trial number and its timing, which marks the beginning of the trial.
            We also have the timing information where we are expecting the effect (sensor information).
            The difference of these two timing information in each trial gives us the delay in each trial.
            And we can plot the histogram of these delay values in each trial over the period of whole experiment
        """

        # shape the data in the right way
        dd = np.array(self.values).reshape(shape)

        # get the time of the start of a trial (a row/column vector)
        trial_start = np.diff(dd[:, trial_index]) if trial_index else np.diff(dd[:, -1])
        trial_start = np.insert(trial_start, 0, 0)
        trial_start_time = dd[trial_start==1, time_index] if time_index else dd[trial_start==1, 0]

        # get the timing of when the effect was sensed (a row/column vector)

        # smoothen the data (a binary signal)
        dd_smooth = dd[:, effect_index].copy() * 0
        dd_smooth[dd[:, effect_index] >= dd[:, effect_index].mean()] = 5

        # apply a rolling window (sets the  values to the value of right edge)


        effect_start_time =

        # get the timing of the change in signal
        latencies = effect_start_time - trial_start_time

    def extend(self, value):
        self.values.extend(value)
