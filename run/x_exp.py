#! /usr/bin/python
# -*- coding: utf-8 -*-
__author__ = "Osman Baskaya"

"""

"""
import sys
from embedding_utils import *
import task3_utils
from itertools import product
from scipy.spatial.distance import cosine, euclidean, correlation
from collections import defaultdict as dd

embedding_f = sys.argv[1]
test_f = sys.stdin
if len(sys.argv) == 3:
    test_f = sys.argv[2]

#embedding_f = 'rcv1.scode.gz'
#test_f = '../data/trial-data/sentence2phrase.trial.input.txt'

sentences = task3_utils.get_sentences(test_f)
wordset = task3_utils.get_wordset(sentences)

sc_vecs = read_embedding_vectors(embedding_f, wordset)
sys.stderr.write("Embedding file reading done.\n")

def score1(closest):
    """ average of all distances """
    score = 0.5
    dists = [dist for t1, (t2, dist) in closest]
    if len(closest) != 0:
        score = sum(dists) / float(len(dists))
    return score

scores = []
miss = 0
comparison = 0
for i, (s1, s2) in enumerate(sentences):
    score = 0
    d = dd(dict)
    s1 = s1.split()
    s2 = s2.split()
    longer, shorter = (s1, s2) if len(s1) >= len(s2) else (s2, s1)
    for t1, t2 in product(shorter, longer):
        comparison += 1
        if t1 in sc_vecs[0] and t2 in sc_vecs[0]:
            distance = 1 - cosine(sc_vecs[0][t1][0], sc_vecs[0][t2][0])
            d[t1][t2] = distance
        else:
            miss += 1
    closest = [(t1, max(d[t1].viewitems(), key=lambda t: t[1])) for t1 in d]
    #print closest
    score = score1(closest)
    scores.append(score)

sys.stderr.write("{}\t{}/{} (miss/attempt).\n".format(embedding_f, miss, comparison))
scores = np.array(scores)
print '\n'.join(scores.astype(str))
