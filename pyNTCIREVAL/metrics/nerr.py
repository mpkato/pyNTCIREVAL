from .normalized_metric import NormalizedMetric
import numpy as np

class nERR(NormalizedMetric):

    def __init__(self, xrelnum, grades, cutoff):
        super(nERR, self).__init__(xrelnum, grades)
        self.cutoff = cutoff

    def gain(self, idx):
        return self._err_grade(idx)

    def discount(self, idx):
        return 1.0 / self.rank(idx)\
            * np.prod([1.0 - r for r in self.gains])
