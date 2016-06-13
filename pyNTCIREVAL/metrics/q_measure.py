from .ncu import NCU, p_u

class QMeasure(NCU):
    def __init__(self, xrelnum, grades, beta, cutoff=None):
        super(QMeasure, self).__init__(xrelnum, grades, p_u(), beta)
        self.cutoff = cutoff
