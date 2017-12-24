from .ncu import NCU, p_u

class QMeasure(NCU):
    '''
    Q-measure

    See Sakai, T. and Song, R.: Evaluating Diversified Search Results Using Per-intent Graded Relevance, SIGIR 2011.

    Args:
        xrelnum: the number of judged X-rel docs (including 0-rel=judged nonrel).
        grades: a list of the grade for each relevance level (except level 0).
        beta: a parameter for blended ratio
        cutoff: the evaluation metric is computed for from the top to this rank if specified
    '''
    def __init__(self, xrelnum, grades, beta, cutoff=None):
        super(QMeasure, self).__init__(xrelnum, grades, beta, p_u())
        self.cutoff = cutoff
