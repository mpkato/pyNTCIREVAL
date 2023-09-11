from .metric import Metric

class Recall(Metric):
    '''
    Recall

    Args:
        xrelnum: the number of judged X-rel docs (including 0-rel=judged nonrel).
        labeled_ranked_list: a list of tuples, where each tuple contains a document ID and its corresponding relevance score.
    '''
    def __init__(self, xrelnum):
        self.total_positives = sum(xrelnum[1:])

    def compute(self, labeled_ranked_list):
        true_positives = sum(grade for docid, grade in labeled_ranked_list if grade is not None and grade > 0)
        if true_positives == 0:
            return 0.0
        return true_positives / self.total_positives
