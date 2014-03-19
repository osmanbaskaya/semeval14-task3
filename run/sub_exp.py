#! /usr/bin/python
# -*- coding: utf-8 -*-
__author__ = "Osman Baskaya"

"""

"""

import sys
import os
import task3_utils
from fastsubs_utils import read_sub_vectors

sub_file = sys.argv[1]
test_f = sys.stdin
if len(sys.argv) == 3:
    test_f = sys.argv[2]

sentences = task3_utils.get_sentences(test_f)
wordset = task3_utils.get_wordset(sentences)

sc_vecs = read_sub_vectors(sub_file, wordset)
sys.stderr.write("Substitute file reading done.\n")
