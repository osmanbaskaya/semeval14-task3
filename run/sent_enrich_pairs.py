#! /usr/bin/python
# -*- coding: utf-8 -*-

__author__ = "Osman Baskaya"

import sys
from itertools import count

c = count(1)

def scode_format(sent, X):
    sent = sent.split()
    for Y in sent:
        print "{}\t{}".format(X, Y)

for sent in sys.stdin:
    scode_format(sent, "S%d" % c.next())
