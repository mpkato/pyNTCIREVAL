from .normalized_metric import NormalizedMetric
import numpy as np

class nERR(NormalizedMetric):
    '''
    normalized Expected Reciprocal Rank

    See Chapelle, O. et al.: Expected Reciprocal Rank for Graded Relevance, CIKM 2009,
    and Sakai, T. and Song, R.: Evaluating Diversified Search Results Using Per-intent Graded Relevance, SIGIR 2011.

    Args:
        xrelnum: the number of judged X-rel docs (including 0-rel=judged nonrel).
        grades: a list of the grade for each relevance level (except level 0).
        cutoff: the evaluation metric is computed for from the top to this rank if specified
    '''
    def __init__(self, xrelnum, grades, cutoff):
        super(nERR, self).__init__(xrelnum, grades)
        self.cutoff = cutoff

    def gain(self, idx):
        return self._err_grade(idx)

    def discount(self, idx):
        return 1.0 / self.rank(idx)\
            * np.prod([1.0 - r for r in self.gains])
