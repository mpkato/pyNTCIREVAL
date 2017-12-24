from .grade_metric import GradeMetric

class RBP(GradeMetric):
    '''
    Rank-biased Precision

    See Moffat, A. and Zobel, J.: Rank-biased Precision for Measurement of Retrieval Effectiveness, ACM TOIS 27(1), 2008.

    Args:
        xrelnum: the number of judged X-rel docs (including 0-rel=judged nonrel).
        grades: a list of the grade for each relevance level (except level 0).
        pr: persistence parameter
    '''

    def __init__(self, xrelnum, grades, pr):
        super(RBP, self).__init__(xrelnum, grades)
        self.pr = pr

    def gain(self, idx):
        return self._rbp_grade(idx)

    def discount(self, idx):
        return (1 - self.pr) * self.pr ** (self.rank(idx) - 1)
