# -*- coding:utf-8 -*-
import pytest
from pyNTCIREVAL.metrics import Metric

class TestMetric(object):

    def test_find_first_rel_rank(self, ranked_list):
        rank = Metric.find_first_rel_rank(ranked_list)
        assert rank == 2

    def test_find_first_max_rank(self, ranked_list):
        rank = Metric.find_first_max_rank(ranked_list)
        assert rank == 3

    @pytest.fixture
    def ranked_list(self):
        return [(1, 0), (2, 2), (3, 3), (2, 2)]
