from .grade_metric import GradeMetric

class OMeasure(GradeMetric):
    '''
    O-measure

    See Sakai, T.: On the Properties of Evaluation Metrics for Finding One Highly Relevant Document,
    IPSJ TOD, Vol.48, No.SIG9 (TOD35), 2007.

    Args:
        xrelnum: the number of judged X-rel docs (including 0-rel=judged nonrel).
        grades: a list of the grade for each relevance level (except level 0).
        beta: a parameter for blended ratio
    '''

    def __init__(self, xrelnum, grades, beta):
        super(OMeasure, self).__init__(xrelnum, grades)
        self.beta = beta
        self.ideal_grade_ranked_list = self._get_ideal_grade_ranked_list()

    def gain(self, idx):
        rank = self.rank(idx)
        g = self._grade(idx)
        ig = sum(self.ideal_grade_ranked_list[:rank])
        return (1 + self.beta * g) / (rank + self.beta * ig)

    def discount(self, idx):
        if self.rank(idx) == self.first_rel_rank:
            return 1.0
        else:
            return 0.0
