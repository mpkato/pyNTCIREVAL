from .ncu import NCU, p_u

class AP(NCU):
    '''
    Average Precision

    See, for example, these papers for details.
    - Sakai, T.: Alternatives to Bpref, SIGIR 2007.
    - Sakai. T. and Robertson, S.: Modelling A User Population for Designing Information Retrieval Metrics, EVIA 2008.

    In this implementation, AP is implemented as a special case of NCU.

    Args:
        xrelnum: the number of judged X-rel docs (including 0-rel=judged nonrel).
        grades: a list of the grade for each relevance level (except level 0).
        cutoff: the evaluation metric is computed for from the top to this rank if specified
    '''
    def __init__(self, xrelnum, grades, cutoff=None):
        super(AP, self).__init__(xrelnum, grades, 0.0, p_u())
        self.cutoff = cutoff
