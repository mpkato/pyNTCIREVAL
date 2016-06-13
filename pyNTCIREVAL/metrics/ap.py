from .ncu import NCU, p_u

class AP(NCU):
    def __init__(self, xrelnum, grades, cutoff=None):
        super(AP, self).__init__(xrelnum, grades, p_u(), 0.0)
        self.cutoff = cutoff
