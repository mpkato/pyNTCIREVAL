from .metric import Metric

class Hit(Metric):
    '''
    1 if top k contains a relevant doc, and 0 otherwise.

    Args:
        cutoff: the evaluation metric is computed for from the top to this rank if specified
    '''
    def __init__(self, cutoff):
        self.cutoff = cutoff

    def gain(self, idx):
        return 1.0 if self._is_relevant(idx) else 0.0

    def discount(self, idx):
        if all([g == 0 for g in self.gains]):
            return 1.0
        else:
            return 0.0
