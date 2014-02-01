#! /usr/bin/python
# -*- coding: utf-8 -*-

__author__ = "Osman Baskaya"

from optparse import OptionParser
import sys
from nltk.corpus import stopwords

parser = OptionParser()
parser.add_option("-l", "--lemmatize", action="store_true", dest="lemmatize", 
            default=False, help="Do you want some lemmatization?")
parser.add_option("-r", "--remove_stop", action="store_true", dest="remove_stop", 
            default=False, help="This option removes all function words using XXX")
parser.add_option("-c", "--lowercase", action="store_true", dest="lower", 
            default=False, help="Make lowercase all tokens in input")

(options, args) = parser.parse_args()

if not any([options.lemmatize, options.remove_stop, options.lower]):
    parser.print_help()
    exit(-1)

swords = set(stopwords.words('english'))
#FIXME: You may want to add PTB tags as well.
for line in sys.stdin:
    s1, s2 = line.split('\t')[:2]
    print " ".join([tok for tok in s1.split() if tok not in swords]),
    print "\t{}".format(' '.join([tok for tok in s2.split() if tok not in swords]))
