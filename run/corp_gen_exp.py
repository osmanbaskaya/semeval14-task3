#! /usr/bin/python
# -*- coding: utf-8 -*-

__author__ = "Osman Baskaya"

import sys

fn = sys.argv[1] # input file
sent_id_fn = sys.argv[2] # the file that contains the sent ids (start and end)
data = open(fn).readlines()



for line in open(sent_id_fn):
    start, end = map(int, line.split())
    print data[start:end]
    exit()
