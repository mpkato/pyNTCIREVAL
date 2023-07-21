from .metric import Metric

class Recall(Metric):
    def __init__(self, total_positive):
        self.total_positives = total_positive

    def compute(self, labeled_ranked_list):
        true_positives = sum(item[1] if item[1] is not None else 0 for item in labeled_ranked_list)
        if true_positives == 0:
            return 0.0
        return true_positives / self.total_positives