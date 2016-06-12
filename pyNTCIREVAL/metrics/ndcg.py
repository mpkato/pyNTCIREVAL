import math
from .normalized_metric import NormalizedMetric

class nDCG(NormalizedMetric):
    def __init__(self, xrelnum, grades, logb, cutoff):
        super(nDCG, self).__init__(xrelnum, grades)
        self.logb = logb
        self.cutoff = cutoff

    def gain(self, grade):
        return self._get_level(grade)

    def discount(self, rank, gains, discounts):
        return (1 + math.log(rank, self.logb))
