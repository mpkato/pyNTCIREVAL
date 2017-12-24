from .metric import Metric

class GradeMetric(Metric):
    '''
    A metric class for all the metrics with graded relevance.

    Args:
        xrelnum: the number of judged X-rel docs (including 0-rel=judged nonrel).
        grades: a list of the grade for each relevance level (except level 0).
    '''

    def __init__(self, xrelnum, grades):
        self.xrelnum = xrelnum
        self.jrelnum = sum(xrelnum[1:])
        self.grades = grades
        self.maxgrade = self.grades[-1]
        self.cutoff = None

    def _grade(self, idx):
        '''
        A grade at idx.

        Args:
            idx: an index of a ranked list

        Returns:
            A grade at idx.
        '''
        level = self._level(idx)
        if level == 0:
            return 0.0
        else:
            return self.grades[level-1]

    def _err_grade(self, idx):
        '''
        An ERR grade at idx.

        Args:
            idx: an index of a ranked list

        Returns:
            An ERR grade at idx.
        '''
        return self._grade(idx) / (self.maxgrade + 1.0)

    def _rbp_grade(self, idx):
        '''
        A RBP grade at idx.

        Args:
            idx: an index of a ranked list

        Returns:
            A RBP grade at idx.
        '''
        return self._grade(idx) / self.maxgrade

    def _get_ideal_grade_ranked_list(self):
        '''
        Get the ideal ranked list of grades.

        Returns:
            Returns a list of grades sorted in the descending order.
            Note that this method does not return
            a ranked list of tuples of a document ID and a relevance level.
        '''
        result = []
        for level, num in enumerate(self.xrelnum):
            if level == 0:
                continue
            result += [self.grades[level-1] for i in range(num)]
        result = sorted(result, reverse=True)
        return result

