from .grade_metric import GradeMetric
import types

class NCU(GradeMetric):
    '''
    NCU (Normalised Cumulative Utility)

    See Sakai. T. and Robertson, S.: Modelling A User Population for Designing Information Retrieval Metrics, EVIA 2008.

    Args:
        xrelnum: the number of judged X-rel docs (including 0-rel=judged nonrel).
        grades: a list of the grade for each relevance level (except level 0).
        beta: a parameter for blended ratio
        sp: a stop probability function. There are three functions in our
            implementation, uniform (p_u), graded-uniform (p_gu), rank-biased (p_rb).
    '''
    def __init__(self, xrelnum, grades, beta, sp):
        super(NCU, self).__init__(xrelnum, grades)
        self.beta = beta
        self.sp = types.MethodType(sp, self)
        self.ideal_grade_ranked_list = self._get_ideal_grade_ranked_list()

    def gain(self, idx):
        '''
        Blended ratio
        '''
        rank = self.rank(idx)
        g = sum([self._grade(i) for i in range(rank)])
        ig = sum(self.ideal_grade_ranked_list[:rank])
        return (self.relnum + self.beta * g) / (rank + self.beta * ig)

    def discount(self, idx):
        return self.sp(idx)

def p_u():
    '''
    Uniform stop probability function
    where the stop probability is the same for all the relevant documents,
    i.e. 1/(# relevant documents).
    '''
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
    '''
    Graded-uniform stop probability function
    where the stop probability is defined for each relevance level.

    Args:
        stops: a list of the stop probability for each relevance level (except 0 level).
    '''
    def func(self, idx):
        level = self._level(idx)
        if level > 0:
            return stops[level-1]\
                / sum([num * stops[l-1]
                    for l, num in enumerate(self.xrelnum) if l > 0])
        else:
            return 0.0
    return func

def p_rb(gamma):
    '''
    Rank-biased stop probability function
    where the stop probability increases
    as the number of preceding relevant documents increase.

    Args:
        gamma: a parameter that controls the gain of the stop probability
            when a relevant document is observed.
    '''
    def func(self, idx):
        if self._is_relevant(idx):
            return gamma ** (self.relnum - 1)\
                / sum([gamma ** i for i in range(self.jrelnum)])
        else:
            return 0.0
    return func

class NCUguP(NCU):
    '''
    NCU (Normalised Cumulative Utility)
    with Pr = Graded-uniform and NU = Precision

    See Sakai. T. and Robertson, S.: Modelling A User Population for Designing Information Retrieval Metrics, EVIA 2008.

    Args:
        xrelnum: the number of judged X-rel docs (including 0-rel=judged nonrel).
        grades: a list of the grade for each relevance level (except level 0).
        stops: a list of the stop probability for each relevance level (except 0 level).
    '''
    def __init__(self, xrelnum, grades, stops):
        super(NCUguP, self).__init__(xrelnum, grades, 0.0, p_gu(stops))

class NCUguBR(NCU):
    '''
    NCU (Normalised Cumulative Utility)
    with Pr = Graded-uniform and NU = Blended ratio

    See Sakai. T. and Robertson, S.: Modelling A User Population for Designing Information Retrieval Metrics, EVIA 2008.

    Args:
        xrelnum: the number of judged X-rel docs (including 0-rel=judged nonrel).
        grades: a list of the grade for each relevance level (except level 0).
        stops: a list of the stop probability for each relevance level (except 0 level).
        beta: a parameter for blended ratio
    '''
    def __init__(self, xrelnum, grades, stops, beta):
        super(NCUguBR, self).__init__(xrelnum, grades, beta, p_gu(stops))

class NCUrbP(NCU):
    '''
    NCU (Normalised Cumulative Utility)
    with Pr = Rank-biased and NU = Precision

    See Sakai. T. and Robertson, S.: Modelling A User Population for Designing Information Retrieval Metrics, EVIA 2008.

    Args:
        xrelnum: the number of judged X-rel docs (including 0-rel=judged nonrel).
        grades: a list of the grade for each relevance level (except level 0).
        gamma: a parameter that controls the gain of the stop probability
            when a relevant document is observed.
    '''
    def __init__(self, xrelnum, grades, gamma):
        super(NCUrbP, self).__init__(xrelnum, grades, 0.0, p_rb(gamma))

class NCUrbBR(NCU):
    '''
    NCU (Normalised Cumulative Utility)
    with Pr = Rank-biased and NU = Blended ratio

    See Sakai. T. and Robertson, S.: Modelling A User Population for Designing Information Retrieval Metrics, EVIA 2008.

    Args:
        xrelnum: the number of judged X-rel docs (including 0-rel=judged nonrel).
        grades: a list of the grade for each relevance level (except level 0).
        gamma: a parameter that controls the gain of the stop probability
            when a relevant document is observed.
        beta: a parameter for blended ratio
    '''
    def __init__(self, xrelnum, grades, gamma, beta):
        super(NCUrbBR, self).__init__(xrelnum, grades, beta, p_rb(gamma))
