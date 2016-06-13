# -*- coding:utf-8 -*-
import sys, os
import unittest
from pyNTCIREVAL.metrics import Metric

class MetricTestCase(unittest.TestCase):
    def setUp(self):
        self.ranked_list = [(1, 0), (2, 2), (3, 3), (2, 2)]

    def test_find_first_rel_rank(self):
        rank = Metric.find_first_rel_rank(self.ranked_list)
        self.assertEqual(rank, 2)

    def test_find_first_max_rank(self):
        rank = Metric.find_first_max_rank(self.ranked_list)
        self.assertEqual(rank, 3)

