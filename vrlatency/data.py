import csv


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

    def analyze(self):
        raise NotImplementedError

    def extend(self, value):
        self.values.extend(value)
