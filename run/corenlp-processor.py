#! /usr/bin/python
# -*- coding: utf-8 -*-
__author__ = "Osman Baskaya"

"""
a
"""

import sys
import os
from bs4 import BeautifulSoup

input_dir = sys.argv[1]
output_fn = input_dir.replace("corenlp-", "")

files = sorted(os.listdir(input_dir), key=lambda fn: int(fn[:-4]))

def lemma_process(sentences):
    L = []
    last = len(sentences) - 1
    for i, sentence in enumerate(sentences):
        lemmas = sentence.findAll('lemma')
        lemmas = [lemma.text for lemma in lemmas]
        if i != last:
            L.append(u' '.join(lemmas))
        else:
            L.append(u'\t%s\n' % (' '.join(lemmas)))
    return L

def token_process(sentence):
    T = []
    last = len(sentences) - 1
    for i, sentence in enumerate(sentences):
        words = sentence.findAll('word')
        words = [word.text for word in words]
        if i != last:
            T.append(u' '.join(words))
        else:
            T.append(u'\t%s\n' % (' '.join(words)))
    return T

#TODO: implement
def dep_parse_process(sentence):
    D = []
    last = len(sentences) - 1
    for i, sentence in enumerate(sentences):
        deps = sentence.findAll('dependencies')
        for dependency in deps:
            if dependency['type'] == 'basic-dependencies': # skip others.
                break
            for dep in dependency:
                gov = dep.find('governor')
                dept = dep.find('dependent') 
                app = u'{} {} {} {} {}'
                L.append(app.format(dep['type'], gov.text, gov['idx'], \
                                                dept.text, dept['idx']))
    
out_files = map(lambda x: open("data/%s.%s.tsv" % (output_fn, x), 'w'), "lem tok".split())

for fn in files:
    sys.stderr.write("%s processing.\n" % fn)
    f = open(os.path.join(input_dir, fn))
    soup =  BeautifulSoup(f, 'xml')
    sentences = soup.findAll('sentence')
    T = token_process(sentences)
    L = lemma_process(sentences)
    out_files[0].write(''.join(L).encode('utf-8'))
    out_files[1].write(''.join(T).encode('utf-8'))

map(lambda f: f.close(), out_files)
