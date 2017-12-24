from .metric import Metric

class RR(Metric):
    def gain(self, idx):
        return 1.0 / self.rank(idx)

    def discount(self, idx):
        if self.rank(idx) == self.first_rel_rank:
            return 1.0
        else:
            return 0.0
