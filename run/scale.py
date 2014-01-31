#! /usr/bin/python
# -*- coding: utf-8 -*-
__author__ = "Osman Baskaya"

"""
Make min-max scaling for the input.
Task3 scoring scheme is in [0,4]

Input:
======
score1\n
score2\n
score3\n
...

"""
import sys
import numpy as np

minimum, maximum = map(float, sys.argv[1:])

array = []
for line in sys.stdin:
    array.append(line.strip())

array = np.array(array, dtype='float64')
array = (maximum - minimum)*((array - array.min()) / (array.max() - array.min())) + minimum
print '\n'.join(map(str, array))
