#! /usr/bin/python
# -*- coding: utf-8 -*-

__author__ = "Osman Baskaya"

import sys
from task3_utils import get_sentences
from itertools import product

fn = sys.argv[1]
sent_fn = sys.argv[2]
data = get_sentences(fn)

c = 0

f = open("%s.sentid" % sent_fn, 'w')
for left, right in data:
    left = left.split()
    right = right.split()
    start = c 
    for tok_left, tok_right in product(left, right):
        print "{}\t{}".format(tok_left, tok_right)
        c += 1
    f.write("{}\t{}\n".format(start, c-1))

f.close()
