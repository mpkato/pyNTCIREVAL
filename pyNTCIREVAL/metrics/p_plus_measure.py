from .grade_metric import GradeMetric

class PPlusMeasure(GradeMetric):
    '''
    P+

    See Sakai, T.: On the Properties of Evaluation Metrics for Finding One Highly Relevant Document,
    IPSJ TOD, Vol.48, No.SIG9 (TOD35), 2007.

    Args:
        xrelnum: the number of judged X-rel docs (including 0-rel=judged nonrel).
        grades: a list of the grade for each relevance level (except level 0).
        beta: a parameter for blended ratio
    '''

    def __init__(self, xrelnum, grades, beta):
        super(PPlusMeasure, self).__init__(xrelnum, grades)
        self.beta = beta
        self.ideal_grade_ranked_list = self._get_ideal_grade_ranked_list()

    def gain(self, idx):
        rank = self.rank(idx)
        g = sum([self._grade(i) for i in range(rank)])
        ig = sum(self.ideal_grade_ranked_list[:rank])
        return (self.relnum + self.beta * g) / (rank + self.beta * ig)

    def discount(self, idx):
        if self._is_relevant(idx)\
            and self.rank(idx) <= self.first_max_rank:
            return 1.0 / len([i for i in range(self.first_max_rank)
                if self._is_relevant(i)])
        else:
            return 0.0

