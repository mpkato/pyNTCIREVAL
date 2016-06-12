class Metric(object):

    def __init__(self, xrelnum, grades):
        self.xrelnum = xrelnum
        self.jrelnum = sum(xrelnum[1:])
        self.grades = grades
        self.cutoff = None

    def compute(self, ranked_list):
        result = 0.0
        gains = []
        discounts = []
        for idx, (did, grade) in enumerate(ranked_list):
            rank = idx + 1
            g = self.gain(grade)
            d = self.discount(rank, gains, discounts)
            result += g / d
            gains.append(g)
            discounts.append(d)

            # cutoff
            if self.cutoff and rank >= self.cutoff:
                break
        return result

    def _get_level(self, grade):
        if grade is None or grade == 0:
            return 0.0
        else:
            return self.grades[grade-1]
