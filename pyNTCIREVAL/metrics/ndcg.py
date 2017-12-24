import math
from .normalized_metric import NormalizedMetric

class nDCG(NormalizedMetric):
    def __init__(self, xrelnum, grades, logb, cutoff):
        super(nDCG, self).__init__(xrelnum, grades)
        self.logb = logb
        self.cutoff = cutoff

    def gain(self, idx):
        return self._grade(idx)

    def discount(self, idx):
        return 1.0 / self._orig_dcglog(self.rank(idx))

    def _orig_dcglog(self, rank):
        '''
        This is for computing the ORIGINAL dcg [Jarvelin/Kekalainen TOIS02].
        if i == 1:
            return 1 (i.e. no discounting)
        if i < b:
            return 1 (i.e. no discounting)
        else (Discounting is applied only if i >= b. )
            return either logb(i)
        '''
        if rank == 1:
            return 1.0
        elif rank < self.logb:
            return 1.0
        else:
            return math.log(rank, self.logb)
