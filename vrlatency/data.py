import csv


class Data(object):
    """ Data object handling data-related matters

    Attributes:
        values: stores the recorded data during the experiment (if record is set to True, and there exist a recording device)
    """

    def __init__(self):
        self.values = []

    def _write_header():
        raise NotImplementedError

    def _write_data(file_obj, data, fieldnames):
        writer = DictWriter(file_obj, delimiter=',', fieldnames=fieldnames)
        writer.writeheader()

        list_of_dicts = []
        for values in data:
            inner_dict = dict(zip(fieldnames, values))
            list_of_dicts.append(inner_dict)

        for dicts in list_of_dicts:
            writer.writerow(dicts)


    def to_csv(self, path, experiment_params=None, data_culomns=None):
        """ Save data into a csv file"""

        # write the experiment parameters (header)
        with open(path, "w"):
            header = ['{}: {}\n'.format(key, value) for key, value in experiment_params.items()]
            csv_file.writelines(header)

            # check if data_culons are empty use integer indecies
            self._write_data(csv_file, data, data_culomns)


    def analyze(self):
        raise NotImplementedError

    def extend(self, value):
        self.values.extend(value)
