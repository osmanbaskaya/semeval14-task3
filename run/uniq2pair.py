#! /usr/bin/python
# -*- coding: utf-8 -*-
__author__ = "Osman Baskaya"

"""

"""

import sys
from nlp_utils import fopen

input_f = sys.argv[1]

prob_d = dict()

for line in sys.stdin:
    L = line.split()
    pairs = '\t'.join(L[3:5])
    prob_d[pairs] = line

for line in fopen(input_f):
    L = line.split()
    pairs = '\t'.join(L[:2])
    print prob_d[pairs],
