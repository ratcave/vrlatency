

class Data(object):
    """ Data object handling data-related matters

    Attributes:
        _array: stores the recorded data during the experiment (if record is set to True, and there exist a recording device)

    """

    def __init__(self):
        self.values = []

    def to_csv(self):
        raise NotImplementedError()

        # dd = np.array(data).reshape(-1, 3)
        # df = pd.DataFrame(data=dd, columns=['Time', "Chan1", 'Trial'])
        # df.to_csv('../Measurements/' + filename + '.csv', index=False)

    def analyze(self):
        raise NotImplementedError()