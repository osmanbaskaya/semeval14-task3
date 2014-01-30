#! /usr/bin/python
# -*- coding: utf-8 -*-
__author__ = "Osman Baskaya"

"""
This module provides some functionality related to S-CODE vectors
such as reading, vector concetanation and so on.
"""

from nlp_utils import fopen
from collections import Counter, defaultdict as dd
import numpy as np
import sys
import gzip

def read_scode_vectors(scode_f, wordset=None):
    """ word_set is a set that indicates the tokens to fetch
        from scode file.
    """
    assert isinstance(wordset, set), "wordset should be a set"

    d = dd(lambda: dict())
    for line in fopen(scode_f):
       line = line.split()
       typ = int(line[0][0])
       w = line[0][2:]
       if wordset is None or w in wordset :
           d[typ][w] = (np.array(line[2:], dtype='float64'), int(line[1]))
    return d

def concat_XY(scode_d, subs):
    d = dd(lambda : dict())
    for X, s in subs.viewitems():
        Xs = Counter(s)
        for Y, count in Xs.viewitems():
            d[X][Y] = (np.concatenate([scode_d[0][X][0], scode_d[1][Y][0]]), count)
    return d

def concat_XYbar(scode_d, subs, dim=25):
    d = dict()
    for X, s in subs.viewitems():
        Y_bar = np.zeros(dim)
        Xs = Counter(s)
        for Y, count in Xs.viewitems():
            Y_bar += scode_d[1][Y][0] * count
        Y_bar /= (Y_bar.dot(Y_bar) ** 0.5)
        d[X] = (np.concatenate(scode_d[0][X][0], Y_bar), 1)
    return d

def write_vec(scode_d, fn=None):
    f = sys.stdout
    if fn is not None:
        f = gzip.open(fn, 'w')
    for word, (vec, count) in scode_d.viewitems():
        f.write("{}\t{}\t{}".format(word, count, "\t".join(map(str, vec))))

    if fn is not None:
        f.close()
