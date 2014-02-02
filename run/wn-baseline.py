#! /usr/bin/python
# -*- coding: utf-8 -*-
__author__ = "Osman Baskaya"

"""

"""

import sys
from nltk.corpus import wordnet as wn
from itertools import product
import task3_utils
from wn_utils import get_synsets_for_sents_tuple
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

syns_sents = get_synsets_for_sents_tuple(sentences)
IC = nltk.corpus.wordnet_ic.ic('ic-brown.dat')
for i, (s1, s2) in enumerate(syns_sents):
    longer, shorter = (s1, s2) if len(s1) >= len(s2) else (s2, s1)
    for syns1, syns2 in product(shorter, longer):
        for syn1, syn2 in product(syns1, syns2):
            distance =  syn1, syn2
            exit()

print >> sys.stderr, "{} line processed".format(i+1)
