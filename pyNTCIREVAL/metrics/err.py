from .grade_metric import GradeMetric
import numpy as np

class ERR(GradeMetric):
    '''
    Expected Reciprocal Rank

    See Chapelle, O. et al.: Expected Reciprocal Rank for Graded Relevance, CIKM 2009.

    Args:
        xrelnum: the number of judged X-rel docs (including 0-rel=judged nonrel).
        grades: a list of the grade for each relevance level (except level 0).
    '''
    def gain(self, idx):
        return self._err_grade(idx)

    def discount(self, idx):
        return 1.0 / self.rank(idx)\
            * np.prod([1.0 - r for r in self.gains])
