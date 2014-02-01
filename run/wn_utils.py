#! /usr/bin/python
# -*- coding: utf-8 -*-
__author__ = "Osman Baskaya"

"""
Useful functions for Wordnet 3.0
"""

import sys
from nltk.corpus import wordnet as wn

w_synsets = dict()

def get_synsets_for_sent(sentence):

    if not isinstance(sentence, list):
        sentence = sentence.split()

    s = []
    for token in sentence:
        if token in w_synsets:
            synsets = w_synsets[token]
        else:
            synsets = wn.synsets(token)
            w_synsets[token] = synsets
        s.append(synsets)

    return s

def get_synsets_for_sents(sentences):
    syns_sents = []
    for sentence in sentences:
        syns_sents.append(get_synsets_for_sent(sentence))
    return syns_sents


def get_synsets_for_sents_tuple(sents_tuples):
    """ This function is for task3 """
    syns_sents = []
    for s1, s2 in sents_tuples:
        syns1 = get_synsets_for_sent(s1)
        syns2 = get_synsets_for_sent(s2)
        syns_sents.append((syns1, syns2))
    sys.stderr.write("all synsets are fetched.\n")
    return syns_sents
