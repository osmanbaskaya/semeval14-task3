#! /usr/bin/python
# -*- coding: utf-8 -*-

__author__ = "Osman Baskaya"


import sys
import random
from nltk.corpus import stopwords


initial = sys.argv[1] # L or R
n = int(sys.argv[2]) # number of substitutes
s = int(sys.argv[3]) # seed

random.seed(s)

stop = set(stopwords.words('english'))
map(stop.add, "lrb rrb rsb . ... , .. ? ` ' ! lsb lcb rcb -LRB- -RRB- -RSB- -LSB- -LCB- \
                -RCB- @card@ n't 's".split())

c = 1

for line in sys.stdin:
    tokens = line.split()
    i = 0
    word = tokens[0]
    if word == '</s>':
        c += 1
        continue
    if word not in stop:
        while i < n:
            total = 0
            for j in range(1, len(tokens), 2):
                tok, p = tokens[j], 10 ** float(tokens[j+1])
                total += p
                if total * random.random() <= p:
                    sub = tok
            print "{}{}\t{}".format(initial, c, sub)
            i += 1
