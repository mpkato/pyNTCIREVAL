from .metric import Metric
import numpy as np

class ERR(Metric):
    def gain(self, idx):
        return self._err_level(idx)

    def discount(self, idx):
        return 1.0 / self._rank(idx)\
            * np.prod([1.0 - r for r in self.gains])
