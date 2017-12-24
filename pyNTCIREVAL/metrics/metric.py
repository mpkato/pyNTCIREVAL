class Metric(object):
    '''
    A base class for all the metrics.
    '''
    def __init__(self):
        self.cutoff = None

    def compute(self, ranked_list):
        '''
        Compute the effectiveness score.

        Args:
            ranked_list: a list of tuples of a document ID and a relevance level,
                i.e. [(doc_id, rel_level)].
        Returns:
            The effectiveness score in terms of this evaluation metric.
        '''
        result = 0.0
        # cache with MetricState for efficient computation
        with MetricState(self, ranked_list):
            for idx, _ in enumerate(ranked_list):
                self.relnum += 1 if self._is_relevant(idx) else 0
                g = self.gain(idx)
                d = self.discount(idx)
                result += g * d
                self.gains.append(g)
                self.discounts.append(d)

                # cutoff
                if self.cutoff and self.rank(idx) >= self.cutoff:
                    break
        return result

    def _level(self, idx):
        '''
        A relevance level at idx.

        Args:
            idx: an index of a ranked list

        Returns:
            A relevance level at idx.
        '''
        _, g = self.ranked_list[idx]
        if g is None:
            return 0.0
        else:
            return g

    def _is_relevant(self, idx):
        '''
        Returns True if the document at idx is relevant,
        i.e. the relevance level > 0

        Args:
            idx: an index of a ranked list

        Returns:
            Returns True if the document at idx is relevant,
            i.e. the relevance level > 0
        '''
        level = self._level(idx)
        return level > 0

    @classmethod
    def rank(cls, idx):
        '''
        Rank at idx, i.e. idx+1.

        Args:
            idx: an index of a ranked list

        Returns:
            Rank at idx, i.e. idx+1.
        '''
        return idx + 1

    @classmethod
    def find_first_rel_rank(cls, ranked_list):
        '''
        Find the rank of the first relevant document for a given ranked list.

        Args:
            ranked_list: a list of tuples of a document ID and a relevance level,
                i.e. [(doc_id, rel_level)].
        Returns:
            The rank of the first relevant document.
            Note is returned if no relevant document.
        '''
        for idx, (_, g) in enumerate(ranked_list):
            if g is not None and g > 0:
                return cls.rank(idx)
        return None

    @classmethod
    def find_first_max_rank(cls, ranked_list):
        '''
        Find the rank of the first document with the maximum relevance level for a given ranked list.

        Args:
            ranked_list: a list of tuples of a document ID and a relevance level,
                i.e. [(doc_id, rel_level)].
        Returns:
            The rank of the first document with the maximum relevance.
            Note is returned if no relevant document.
        '''
        levels = [l if l is not None else 0 for _, l in ranked_list]
        maxlevel = max(levels)
        if maxlevel > 0:
            idx = levels.index(maxlevel)
            return cls.rank(idx)
        else:
            return None

    def __str__(self):
        '''
        Return the name of the class with the cutoff value.

        Returns:
            The name of the class with the cutoff value.
        '''
        if self.cutoff is None:
            return self.__class__.__name__
        else:
            return "%s@%04d" % (self.__class__.__name__, self.cutoff)

class MetricState(object):
    '''
    This class provides a cache mechanism for evaluation metrics.
    Initializes the cache when it is initialized,
    and discards the cache when it exists.

    Examples:
        with MetricState(self, ranked_list):
            # The cache is initialized.
            # Do something with the cache.
        # The cache is discarded here.
    '''

    def __init__(self, metric, ranked_list):
        self.metric = metric
        self.ranked_list = ranked_list

    def __enter__(self):
        '''
        Initializes all the caches.
        '''
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
        '''
        Discards all the caches.
        '''
        del self.metric.gains
        del self.metric.discounts
        del self.metric.relnum
        del self.metric.ranked_list
        del self.metric.syslen
        del self.metric.first_rel_rank
        del self.metric.first_max_rank
