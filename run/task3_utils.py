#! /usr/bin/python
# -*- coding: utf-8 -*-
__author__ = "Osman Baskaya"

"""

"""

import sys
import os
from nlp_utils import fopen

def get_sentences(fn):
    """ This method for
            - paragraph2sentence
            - sentence2phrase
            - phrase2word
    """
    sentences = []
    for line in fopen(fn):
        line = line.split('\t')
        s1, s2 = line[0], line[1].strip()
        sentences.append((s1, s2))
    sys.stderr.write("{} sentences fetched.\n".format(len(sentences)))
    return sentences

def get_wordset(sentences):
    s = set()
    for s1, s2 in sentences:
        map(s.add, s1.split())
        map(s.add, s2.split())
    sys.stderr.write("{} unique tokens.\n".format(len(s)))
    return s
