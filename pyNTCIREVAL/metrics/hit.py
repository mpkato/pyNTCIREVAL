from .metric import Metric

class Hit(Metric):

    def __init__(self, xrelnum, grades, cutoff):
        super(Hit, self).__init__(xrelnum, grades)
        self.cutoff = cutoff

    def gain(self, idx):
        return 1.0 if self._is_relevant(idx) else 0.0

    def discount(self, idx):
        if all([g == 0 for g in self.gains]):
            return 1.0
        else:
            return 0.0
