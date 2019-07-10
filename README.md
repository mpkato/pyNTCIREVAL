# pyNTCIREVAL

[![CircleCI](https://circleci.com/gh/mpkato/pyNTCIREVAL.svg?style=svg)](https://circleci.com/gh/mpkato/pyNTCIREVAL)

## Introduction

pyNTCIREVAL is a python version of NTCIREVAL http://research.nii.ac.jp/ntcir/tools/ntcireval-en.html
developed by Dr. Tetsuya Sakai http://www.f.waseda.jp/tetsuya/sakai.html .
Only a part of NTCIREVAL functionalities has been implemented in the current
version of pyNTCIREVAL:
retrieval effectiveness metrics for ranked retrieval (e.g. DCG and ERR).
As shown below, pyNTCIREVAL can be used in Python codes as well.

For Japanese users, there is a very nice textbook written in Japanese
that discusses various evaluation metrics and how to use NTCIREVAL: see http://www.f.waseda.jp/tetsuya/book.html .

## Evaluation Metrics

These evaluation metrics are available in the current version:

- Hit@k: 1 if top k contains a relevant doc, and 0 otherwise.
- P@k (precision at k): number of relevant docs in top k divided by k.
- AP (Average Precision)<sup>6, 7</sup>.
- ERR (Expected Reciprocal Rank), nERR@k<sup>2, 8</sup>.
- RBP (Rank-biased Precision)<sup>4</sup>.
- nDCG (original nDCG)<sup>3</sup>.
- MSnDCG (Microsoft version of nDCG)<sup>1</sup>.
- Q-measure<sup>8</sup>.
- RR (Reciprocal Rank).
- O-measure<sup>5</sup>
- P-measure and P-plus<sup>5</sup>.
- NCU (Normalised Cumulative Utility)<sup>7</sup>.

## Installation

```bash
pip install pyNTCIREVAL
```

## Examples

### P@k

```python
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
```

### nDCG@k (Microsoft version)

Many evaluation metric classes need `xrelnum` and `grades` as input for initialization.

`xrelnum` is a list containing the number of documents of i-th relevance level,
while `grades` is a list containing a grade for each i-th relevance level (except for level 0).

For example, there are three levels of relevance: irrelevant, partially relevant, and highly relevant.
Suppose a document collection includes 5 irrelevant, 3 partially relevant, and 2 highly relevant for a certain topic.
In this case, `xrelnum = [5, 3, 2]`.
If we want to assign 0, 1, and 2 grades for each level, then `grades = [1, 2]`.

```python
from pyNTCIREVAL import Labeler
from pyNTCIREVAL.metrics import MSnDCG

# dict of { document ID: relevance level }
qrels = {0: 2, 1: 0, 2: 1, 3: 0, 4: 1, 5: 0, 6: 0, 7: 2, 8: 0, 9: 0} 
grades = [1, 2] # a grade for relevance levels 1 and 2 (Note that level 0 is excluded)
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
assert result == 0.6885695823073614
```


## References

[1] Burges, C. et al.: 
Learning to rank using gradient descent, 
ICML 2005.

[2] Chapelle, O. et al.:
Expected Reciprocal Rank for Graded Relevance,
CIKM 2009.

[3] Jarvelin, K. and Kelalainen, J.:
Cumulated Gain-based Evaluation of IR Techniques,
ACM TOIS 20(4), 2002.

[4] Moffat, A. and Zobel, J.:
Rank-biased Precision for Measurement of Retrieval Effectiveness,
ACM TOIS 27(1), 2008.

[5] Sakai, T.:
On the Properties of Evaluation Metrics for Finding One Highly Relevant Document,
IPSJ TOD, Vol.48, No.SIG9 (TOD35), 2007.

[6] Sakai, T.:
Alternatives to Bpref,
SIGIR 2007.

[7] Sakai. T. and Robertson, S.:
Modelling A User Population for Designing Information Retrieval Metrics,
EVIA 2008.

[8] Sakai, T. and Song, R.:
Evaluating Diversified Search Results Using Per-intent Graded Relevance,
SIGIR 2011.


