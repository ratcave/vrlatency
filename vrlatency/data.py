import csv


class Data(object):
    """ Data object handling data-related matters

    Attributes:
        values: stores the recorded data during the experiment (if record is set to True, and there exist a recording device)
    """

    def __init__(self):
        self.values = []

    def to_csv(self, path):
        """ Save data into a csv file"""
        with open(path, 'w', newline='\n') as file:
            writer = csv.writer(file)
            writer.writerows(self.values)

    def analyze(self):
        raise NotImplementedError

    def extend(self, value):
        self.values.extend(value)
