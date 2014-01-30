#! /usr/bin/python
# -*- coding: utf-8 -*-
__author__ = "Osman Baskaya"

"""

"""
import sys
from scode_utils import *
import task3_utils
from itertools import product
from scipy.spatial.distance import cosine, euclidean, correlation

#scode_f = sys.argv[1]
#test_f = sys.argv[2]

scode_f = 'rcv1.scode.gz'
test_f = '../data/trial-data/sentence2phrase.trial.input.txt'

sentences = task3_utils.get_sentences(test_f)
print sentences[0]
wordset = task3_utils.get_wordset(sentences)

sc_vecs = read_scode_vectors(scode_f, wordset)
sys.stderr.write("S-CODE output reading done.\n")

for i, (s1, s2) in enumerate(sentences):
    d = dd(dict)
    for t1, t2 in product(s1.split(), s2.split()):
        if t1 in sc_vecs[0] and t2 in sc_vecs[0]:
            distance = cosine(sc_vecs[0][t1][0], sc_vecs[0][t2][0])
            d[t1][t2] = distance
    closest = [(t1, min(d[t1], key=lambda t2: d[t1][t2])) for t1 in d]
    print closest
    exit()



        




