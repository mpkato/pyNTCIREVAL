from .metric import Metric
import types

def p_u():
    def func(self, idx):
        if self._is_relevant(idx):
            jrelnum = self.jrelnum
            if self.cutoff:
                jrelnum = min([jrelnum, self.cutoff])
            return 1.0 / jrelnum
        else:
            return 0.0
    return func

def p_gu(stops):
    def func(self, idx):
        grade = self._grade(idx)
        if grade > 0:
            return stops[grade-1]\
                / sum([num * stops[g-1]
                    for g, num in enumerate(self.xrelnum) if g > 0])
        else:
            return 0.0
    return func

def p_rb(gamma):
    def func(self, idx):
        if self._is_relevant(idx):
            return gamma ** (self.relnum - 1)\
                / sum([gamma ** i for i in range(self.jrelnum)])
        else:
            return 0.0
    return func

class NCU(Metric):

    def __init__(self, xrelnum, grades, sp, beta):
        super(NCU, self).__init__(xrelnum, grades)
        self.sp = types.MethodType(sp, self)
        self.beta = beta
        self.ideal_level_ranked_list = self._get_ideal_level_ranked_list()

    def gain(self, idx):
        '''
        BR: blended ratio
        '''
        rank = self._rank(idx)
        g = sum([self._level(i) for i in range(rank)])
        ig = sum(self.ideal_level_ranked_list[:rank])
        return (self.relnum + self.beta * g) / (rank + self.beta * ig)

    def discount(self, idx):
        return self.sp(idx)

class NCUguP(NCU):
    def __init__(self, xrelnum, grades, stops):
        super(NCUguP, self).__init__(xrelnum, grades, p_gu(stops), 0.0)

class NCUguBR(NCU):
    def __init__(self, xrelnum, grades, stops, beta):
        super(NCUguBR, self).__init__(xrelnum, grades, p_gu(stops), beta)

class NCUrbP(NCU):
    def __init__(self, xrelnum, grades, gamma):
        super(NCUrbP, self).__init__(xrelnum, grades, p_rb(gamma), 0.0)

class NCUrbBR(NCU):
    def __init__(self, xrelnum, grades, gamma, beta):
        super(NCUrbBR, self).__init__(xrelnum, grades, p_rb(gamma), beta)
