# -*- coding:utf-8 -*-
import pytest

class TestRecall(object):

    def test_precision(self):
        from pyNTCIREVAL import Labeler
        from pyNTCIREVAL.metrics import Recall
        
        qrels = {0: 1, 1: 0, 2: 0, 3: 0, 4: 1, 5: 0, 6: 0, 7: 1, 8: 0, 9: 0}
        ranked_list = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9] # a list of document IDs

        # labeling: [doc_id] -> [(doc_id, rel_level)]
        labeler = Labeler(qrels)
        labeled_ranked_list = labeler.label(ranked_list)
        
        total_positive = len([{docid, grade} for docid, grade in qrels.items() if grade == 1])
        metric = Recall(total_positive)
        assert total_positive == 3
        
        result = metric.compute(labeled_ranked_list)
        assert result == 1.0