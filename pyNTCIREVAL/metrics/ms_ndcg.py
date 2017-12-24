import math
from .normalized_metric import NormalizedMetric

class MSnDCG(NormalizedMetric):
    def __init__(self, xrelnum, grades, cutoff):
        super(MSnDCG, self).__init__(xrelnum, grades)
        self.cutoff = cutoff

    def gain(self, idx):
        return self._grade(idx)

    def discount(self, idx):
        return 1.0 / math.log(self.rank(idx) + 1)
