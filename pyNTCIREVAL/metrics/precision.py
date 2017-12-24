from .metric import Metric

class Precision(Metric):
    '''
    Precision

    Args:
        cutoff: the evaluation metric is computed for from the top to this rank if specified
    '''

    def __init__(self, cutoff):
        self.cutoff = cutoff

    def gain(self, idx):
        return 1.0 if self._is_relevant(idx) else 0.0

    def discount(self, idx):
        return 1.0 / self.cutoff
