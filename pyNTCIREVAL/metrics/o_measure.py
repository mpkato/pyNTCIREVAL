from .metric import Metric

class OMeasure(Metric):

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
