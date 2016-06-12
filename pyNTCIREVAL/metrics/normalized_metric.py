from .metric import Metric

class NormalizedMetric(Metric):
    def compute(self, ranked_list):
        actual = super(NormalizedMetric, self).compute(ranked_list)
        irl = self.ideal_ranked_list()
        ideal = super(NormalizedMetric, self).compute(irl)
        return actual / ideal

    def ideal_ranked_list(self):
        result = []
        for grade, num in enumerate(self.xrelnum):
            result += [(i, grade)
                for i in range(len(result), len(result)+num)]
        result = sorted(result, key=lambda x: x[1], reverse=True)
        return result
