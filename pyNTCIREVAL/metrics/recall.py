from .metric import Metric

class Recall(Metric):
    def __init__(self, xrelnum):
        self.total_positives = sum(xrelnum[1:])

    def compute(self, labeled_ranked_list):
        true_positives = sum(grade for docid, grade in labeled_ranked_list if grade is not None and grade > 0)
        if true_positives == 0:
            return 0.0
        return true_positives / self.total_positives