#!/usr/bin/python
import gzip, itertools as it
import sys, math
from collections import defaultdict as ddict

def get_wf_lemma(stem_file):
    with open(stem_file) as src:
        return dict([l.strip().split('\t') for l in src])

def get_test_vocab(test_file):
    with open(test_file) as src:
        return set(reduce(lambda x,y:x+y, [l.strip().split('\t')[:-1] for l in src]))

def get_pairs(test_file):
    pairs = ddict(set)
    with open(test_file) as src:
        for lem1, lem2 in [l.strip().split('\t')[:-1] for l in src]:
            pair = ' '.join([lem1,lem2])
            pairs[lem1].add(pair)
            pairs[lem2].add(pair)
    return pairs

def main(args):
    wf_lemma = get_wf_lemma(args.stem_file)
    test_vocab = get_test_vocab(args.test_file)
    pairs = get_pairs(args.test_file)

    plemma = ddict(float)
    ppairs = ddict(float)
    #with gzip.GzipFile(args.sub_gz) as src:
    N = 0
    for l in sys.stdin:
        N += 1
        tuples = map(lambda x: (x[0],float(x[1])), [wf_logp.split(' ') for wf_logp in l.strip().split('\t')[1:]])
        z = sum([10**t[1] for t in tuples])
        logz = math.log10(z)

        pl = ddict(float)
        for wf, logp in tuples:
            if wf in wf_lemma and wf_lemma[wf] in test_vocab:
                normp = 10**(logp - logz) # norm prob
                pl[wf_lemma[wf]] += normp

        #print >> sys.stderr, tuples
        #print >> sys.stderr, pl
        markp = set()
        for lem in pl.keys():
            plemma[lem] += pl[lem]
            markp.update(pairs[lem])

        for pair in markp:
            lem, lem2 = pair.split()
            ppairs[pair] += pl[lem] * pl[lem2]

        #print >> sys.stderr, ppairs
        if not N % 10**4:
            sys.stderr.write('.')

    print >> sys.stderr
    
    with open(args.test_file) as src:
        for lem1, lem2, y in [l.strip().split('\t') for l in src]:
            pair = ' '.join([lem1,lem2])
            print '%g\t%g\t%g\t%s\t%s\t%s'%(plemma[lem1]/N,plemma[lem2]/N,ppairs[pair]/N,lem1,lem2,y)

if __name__ == '__main__':
    import argparse
    parser = argparse.ArgumentParser()
    #parser.add_argument('sub_gz')
    parser.add_argument('stem_file')
    parser.add_argument('test_file')
    main(parser.parse_args())
