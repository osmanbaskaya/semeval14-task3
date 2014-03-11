#! /usr/bin/python
# -*- coding: utf-8 -*-

__author__ = "Osman Baskaya"

import sys
from task3_utils import get_sentences
from itertools import count

p2s_f = sys.argv[1] 
data = get_sentences(p2s_f)

c = count(1)

def scode_format(sent, X):
    sent = sent.split()
    for Y in sent:
        print "{}\t{}".format(X, Y)

for left, right in data:
    num = c.next()
    scode_format(left, "L%d" % num)
    scode_format(right, "R%d" % num)
