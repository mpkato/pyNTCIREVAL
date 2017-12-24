from .metric import Metric

class RBP(Metric):

    def __init__(self, xrelnum, grades, pr):
        super(RBP, self).__init__(xrelnum, grades)
        self.pr = pr

    def gain(self, idx):
        return self._rbp_grade(idx)

    def discount(self, idx):
        return (1 - self.pr) * self.pr ** (self.rank(idx) - 1)
