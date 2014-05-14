#! /usr/bin/python
# -*- coding: utf-8 -*-
__author__ = "Osman Baskaya"

"""

"""

import sys
from nltk.corpus import wordnet as wn
from itertools import product
import task3_utils
import numpy as np
from wn_utils import get_synsets_for_sents_tuple
from collections import defaultdict as dd
import nltk

test_f = sys.stdin

sentences = task3_utils.get_sentences(test_f)
metric_name = sys.argv[1]

if metric_name == "lch":
    metric = wn.lch_similarity
elif metric_name == "lin":
    metric = wn.lin_similarity
elif metric_name == "jcn":
    metric = wn.jcn_similarity
elif metric_name == "path":
    metric = wn.path_similarity
elif metric_name == "wup":
    metric = wn.wup_similarity
elif metric_name == "res":
    metric = wn.res_similarity
else:
    sys.stderr.write("No such similarity metric in WN module.\n")
    exit(-1)

sys.stderr.write("Metric: {0}\n".format(metric.func_name))

def score1(closest):
    score = 0
    dists = [dist for t1, (t2, (dist, s1, s2)) in closest]
    if len(closest) != 0:
        score = sum(dists) / float(len(dists))
    return score

syns_sents = get_synsets_for_sents_tuple(sentences)
unav = set(['a', 's', 'r'])
IC = nltk.corpus.wordnet_ic.ic('ic-brown.dat')
scores = []
for i, (s1, s2) in enumerate(syns_sents):
    #print sentences[i][0]
    #print sentences[i][1]
    longer, shorter = (s1, s2) if len(s1) >= len(s2) else (s2, s1)
    d = dd(dict)
    for syns1, syns2 in product(shorter, longer):
        #print syns1, syns2
        for syn1, syn2 in product(syns1, syns2):
            p1, p2 = syn1.pos, syn2.pos
            if p1 == p2 and p1 not in unav and p2 not in unav:
                sim = metric(syn1, syn2, IC)
                d[syn1.offset][syn2.offset] = (sim, syn1, syn2)
    #FIXME bu hatali olabilir
    closest = [(t1, max(d[t1].iteritems(), key=lambda t: t[1][0])) for t1 in d]
    score = score1(closest)
    scores.append(score)

print >> sys.stderr, "{0} line processed".format(i+1)
#sys.stderr.write("{}/{} (miss/attempt).\n".format(miss, comparison))
scores = np.array(scores)
print '\n'.join(scores.astype(str))
