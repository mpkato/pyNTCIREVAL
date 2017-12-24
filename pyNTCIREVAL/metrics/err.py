from .grade_metric import GradeMetric
import numpy as np

class ERR(GradeMetric):
    def gain(self, idx):
        return self._err_grade(idx)

    def discount(self, idx):
        return 1.0 / self.rank(idx)\
            * np.prod([1.0 - r for r in self.gains])
