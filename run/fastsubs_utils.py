#! /usr/bin/python
# -*- coding: utf-8 -*-
__author__ = "Osman Baskaya"

"""

"""
import sys
from nlp_utils import fopen
from collections import defaultdict as dd


def read_sub_vectors(sub_f, wordset=None):
    """ word_set is a set that indicates the tokens to fetch
        from substitute file.
    """
    assert isinstance(wordset, set) or wordset is None, "wordset should be a set"

    d = dd(list)
    for line in fopen(sub_f):
        line = line.split()
        w = line[0] # 



        if wordset is None or w in wordset :
            d =

    #d[w] = (np.array(line[start:], dtype='float64'), count)

