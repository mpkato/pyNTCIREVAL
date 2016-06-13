from .metric import Metric

class PMeasure(Metric):

    def __init__(self, xrelnum, grades, beta):
        super(PMeasure, self).__init__(xrelnum, grades)
        self.beta = beta
        self.ideal_level_ranked_list = self._get_ideal_level_ranked_list()

    def gain(self, idx):
        rank = self._rank(idx)
        g = sum([self._level(i) for i in range(rank)])
        ig = sum(self.ideal_level_ranked_list[:rank])
        return (self.relnum + self.beta * g) / (rank + self.beta * ig)

    def discount(self, idx):
        if self._rank(idx) == self.first_max_rank:
            return 1.0
        else:
            return 0.0
