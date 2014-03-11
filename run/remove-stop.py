#! /usr/bin/python
# -*- coding: utf-8 -*-

__author__ = "Osman Baskaya"

#tr -cd "[:alpha:] [:space:]" | tr 'A-Z' 'a-z' | ./remove-stop.py 

from nltk.corpus import stopwords
import sys


stop = set(stopwords.words('english'))
map(stop.add, "lrb rrb rsb lsb lcb rcb -LRB- -RRB- -RSB- -LSB- -LCB- -RCB- @card@ \
              n't 's".split())

for line in sys.stdin:
    line = line.split(' ')
    print ' '.join([t for t in line if t not in stop and t != '']),
