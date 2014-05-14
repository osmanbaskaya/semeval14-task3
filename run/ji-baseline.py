#! /usr/bin/python
# -*- coding: utf-8 -*-
__author__ = "Osman Baskaya"

"""
Jaccard Index as a baseline for task3

"""
import sys
import task3_utils

sentences = task3_utils.get_sentences(sys.stdin)

for i, (s1, s2) in enumerate(sentences):
    s1 = set(s1.split())
    s2 = set(s2.split())
    print len(s1.intersection(s2)) / float(len(s1.union(s2)))

print >> sys.stderr, "{0} line processed".format(i+1)
