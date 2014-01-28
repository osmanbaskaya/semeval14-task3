#! /usr/bin/python
# -*- coding: utf-8 -*-

__author__ = "Osman Baskaya"

from optparse import OptionParser
import sys
import nltk

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


