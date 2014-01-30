#! /usr/bin/python
# -*- coding: utf-8 -*-
__author__ = "Osman Baskaya"

"""

"""

import sys
from nlp_utils import fopen
from collections import defaultdict as dd

def get_pairs(pairs_f):
    d = dd(list)
    for line in fopen(pairs_f):
        tw, sub = line.split()
        d[tw].append(sub)
    return d
