import math
from .normalized_metric import NormalizedMetric

class MSnDCG(NormalizedMetric):
    '''
    Microsoft version of normalized discounted cumulative gain.

    See Burges, C. et al.: Learning to rank using gradient descent, ICML 2005.

    Args:
        xrelnum: the number of judged X-rel docs (including 0-rel=judged nonrel).
        grades: a list of the grade for each relevance level (except level 0).
        cutoff: the evaluation metric is computed for from the top to this rank if specified
    '''
    def __init__(self, xrelnum, grades, cutoff):
        super(MSnDCG, self).__init__(xrelnum, grades)
        self.cutoff = cutoff

    def gain(self, idx):
        return self._grade(idx)

    def discount(self, idx):
        return 1.0 / math.log(self.rank(idx) + 1)
