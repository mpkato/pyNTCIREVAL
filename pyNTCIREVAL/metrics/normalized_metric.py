from .grade_metric import GradeMetric

class NormalizedMetric(GradeMetric):
    def compute(self, ranked_list):
        actual = super(NormalizedMetric, self).compute(ranked_list)
        irl = self.get_ideal_ranked_list()
        ideal = super(NormalizedMetric, self).compute(irl)
        return actual / ideal

    def get_ideal_ranked_list(self):
        result = []
        for grade, num in enumerate(self.xrelnum):
            result += [(i, grade)
                for i in range(len(result), len(result)+num)]
        result = sorted(result, key=lambda x: x[1], reverse=True)
        return result
