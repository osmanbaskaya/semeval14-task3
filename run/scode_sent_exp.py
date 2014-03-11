#! /usr/bin/python
# -*- coding: utf-8 -*-

__author__ = "Osman Baskaya"

import sys
from embedding_utils import read_embedding_vectors
import numpy as np

embedding_f = sys.argv[1]

emb = read_embedding_vectors(embedding_f, None)[0]

N = len(emb)

for i in range(1, N/2+1):
    left = emb["L%d" % i][0]
    right = emb["R%d" % i][0]
    print np.dot(left, right)
