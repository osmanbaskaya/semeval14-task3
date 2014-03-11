#! /usr/bin/python
# -*- coding: utf-8 -*-

__author__ = "Osman Baskaya"

from nltk.corpus import brown, gutenberg

for c in [brown, gutenberg]:
    for line in c.sents():
        print ' '.join(line)
