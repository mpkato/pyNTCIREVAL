# -*- coding:utf-8 -*-
import pytest

class TestUsage(object):

    def test_precision(self):
        from pyNTCIREVAL import Labeler
        from pyNTCIREVAL.metrics import Precision

        # dict of { document ID: relevance level }
        qrels = {0: 1, 1: 0, 2: 0, 3: 0, 4: 1, 5: 0, 6: 0, 7: 1, 8: 0, 9: 0}
        ranked_list = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9] # a list of document IDs

        # labeling: [doc_id] -> [(doc_id, rel_level)]
        labeler = Labeler(qrels)
        labeled_ranked_list = labeler.label(ranked_list)
        assert labeled_ranked_list == [
            (0, 1), (1, 0), (2, 0), (3, 0), (4, 1),
            (5, 0), (6, 0), (7, 1), (8, 0), (9, 0)
        ]

        # let's compute Precision@5
        metric = Precision(cutoff=5)
        result = metric.compute(labeled_ranked_list)
        assert result == 0.4

    def test_ms_ndcg(self):
        from pyNTCIREVAL import Labeler
        from pyNTCIREVAL.metrics import MSnDCG

        # dict of { document ID: relevance level }
        qrels = {0: 2, 1: 0, 2: 1, 3: 0, 4: 1, 5: 0, 6: 0, 7: 2, 8: 0, 9: 0} 
        grades = [0, 1, 2] # a grade for each relevance level
        ranked_list = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9] # a list of document IDs

        # labeling: [doc_id] -> [(doc_id, rel_level)]
        labeler = Labeler(qrels)
        labeled_ranked_list = labeler.label(ranked_list)
        assert labeled_ranked_list == [
            (0, 2), (1, 0), (2, 1), (3, 0), (4, 1),
            (5, 0), (6, 0), (7, 2), (8, 0), (9, 0)
        ]

        # compute the number of documents for each relevance level
        rel_level_num = 3
        xrelnum = labeler.compute_per_level_doc_num(rel_level_num)
        assert xrelnum == [6, 2, 2]

        # Let's compute nDCG@5
        metric = MSnDCG(xrelnum, grades, cutoff=5)
        result = metric.compute(labeled_ranked_list)
        assert result == 0.6131471927654584
