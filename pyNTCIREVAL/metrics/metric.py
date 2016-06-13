class Metric(object):

    def __init__(self, xrelnum, grades):
        self.xrelnum = xrelnum
        self.jrelnum = sum(xrelnum[1:])
        self.grades = grades
        self.maxgrade = self.grades[-1]
        self.cutoff = None

    def compute(self, ranked_list):
        result = 0.0
        with MetricState(self, ranked_list):
            for idx, _ in enumerate(ranked_list):
                self.relnum += 1 if self._is_relevant(idx) else 0
                g = self.gain(idx)
                d = self.discount(idx)
                result += g * d
                self.gains.append(g)
                self.discounts.append(d)

                # cutoff
                if self.cutoff and self._rank(idx) >= self.cutoff:
                    break
        return result

    def _grade(self, idx):
        _, g = self.ranked_list[idx]
        if g is None:
            return 0.0
        else:
            return g

    def _level(self, idx):
        grade = self._grade(idx)
        if grade == 0:
            return 0.0
        else:
            return self.grades[grade-1]

    def _err_level(self, idx):
        return self._level(idx) / (self.maxgrade + 1.0)

    def _rbp_level(self, idx):
        return self._level(idx) / self.maxgrade

    def _rank(self, idx):
        return idx + 1

    def _is_relevant(self, idx):
        grade = self._grade(idx)
        return grade > 0

    def _get_ideal_level_ranked_list(self):
        result = []
        for grade, num in enumerate(self.xrelnum):
            if grade == 0:
                continue
            result += [self.grades[grade-1] for i in range(num)]
        result = sorted(result, reverse=True)
        return result

    @classmethod
    def find_first_rel_rank(cls, ranked_list):
        for idx, (_, g) in enumerate(ranked_list):
            if g is not None and g > 0:
                return idx + 1
        return None

    @classmethod
    def find_first_max_rank(cls, ranked_list):
        grades = [g if g is not None else 0 for _, g in ranked_list]
        maxgrade = max(grades)
        if maxgrade > 0:
            return grades.index(maxgrade) + 1
        else:
            return None

    def __str__(self):
        if self.cutoff is None:
            return self.__class__.__name__
        else:
            return "%s@%04d" % (self.__class__.__name__, self.cutoff)

class MetricState(object):

    def __init__(self, metric, ranked_list):
        self.metric = metric
        self.ranked_list = ranked_list

    def __enter__(self):
        self.metric.gains = []
        self.metric.discounts = []
        self.metric.relnum = 0
        self.metric.ranked_list = self.ranked_list
        self.metric.syslen = len(self.ranked_list)
        self.metric.first_rel_rank =\
            Metric.find_first_rel_rank(self.ranked_list)
        self.metric.first_max_rank =\
            Metric.find_first_max_rank(self.ranked_list)

    def __exit__(self, type, value, traceback):
        del self.metric.gains
        del self.metric.discounts
        del self.metric.relnum
        del self.metric.ranked_list
        del self.metric.syslen
        del self.metric.first_rel_rank
        del self.metric.first_max_rank
