# -*- coding:utf-8 -*-
import pytest

class TestRecall(object):

    def test_precision(self):
        from pyNTCIREVAL import Labeler
        from pyNTCIREVAL.metrics import Recall
        
        qrels = {0: 1, 1: 0, 2: 0, 3: 0, 4: 1, 5: 0, 6: 0, 7: 1, 8: 0, 9: 0}
        ranked_list = [0, 1, 3, 5, 8, 9] # a list of document IDs

        # labeling: [doc_id] -> [(doc_id, rel_level)]
        labeler = Labeler(qrels)
        labeled_ranked_list = labeler.label(ranked_list)
        
        xrelnum = labeler.compute_per_level_doc_num(2)
        metric = Recall(xrelnum)
        assert xrelnum == [7, 3]
        
        result = metric.compute(labeled_ranked_list)
        assert result == 0.3333333333333333