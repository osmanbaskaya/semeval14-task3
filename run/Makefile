SHELL := /bin/bash

.SECONDARY:

### PATH
SRILM_PATH=/opt/srilm/bin/i686-m64
CORE_NLP_PATH=../../tools/src/stanford-corenlp

export PATH:=.:../../tools/bin/:${SRILM_PATH}:${PATH}

SEED=1
CPU=2
LM=enw.lm.gz
SCORER= java -jar ../data/evaluation/task-3-scorer.jar

bin:
	cd ../bin; make

enw.lm.gz:
	ln -s /scratch/1/myatbaz/upos_new/run/enw_ukvac2/enw.lm.gz

SC_OPTIONS=-s ${SEED} -v -d 25
%.scode.gz: %.pairs.gz
	zcat $< | scode ${SC_OPTIONS} | gzip > $@

# Stanford CoreNLP is used for tokenization, tagging, and dependency parsing
CORE_NLP=java -mx2g -cp "${CORE_NLP_PATH}/*" edu.stanford.nlp.pipeline.StanfordCoreNLP 
ANNOTATORS=-annotators "tokenize, ssplit, pos, lemma, parse"
CNLP_OPTIONS=${ANNOTATORS} -replaceExtension -threads ${CPU} 
corenlp-%: ../data/data-files/%.input.tsv
	-rm -rf docs; mkdir docs
	cat $< | cut -f1,2 | awk 'BEGIN{i=1}{printf("%s\n", $$0) > "docs/"i++".txt"}'
	${CORE_NLP} ${CNLP_OPTIONS} -outputDirectory $@ -file docs/ 


### BASELINE ###
ans/ji-baseline-%.ans: ../data/data-files/%.input.tsv
	cat $< | ji-baseline.py > $@

ans/wn-baseline-%-sentence2phrase.ans: data/sentence2phrase.train.lem.tsv
	cat $< | data-preprocess.py -l | wn-baseline.py $* > $@
 
ans/wn-baseline-%-paragraph2sentence.ans: data/paragraph2sentence.train.lem.tsv
	cat $< | data-preprocess.py -l | wn-baseline.py $* > $@

GOLD_P2S=../data/keys/paragraph2sentence.train.gs.tsv
GOLD_S2P=../data/keys/sentence2phrase.train.gs.tsv
GOLD_P2W=../data/keys/phrase2word.train.gs.tsv

ans/x_exp-p2s-tr-%-base.ans: ../data/data-files/paragraph2sentence.train.input.tsv embeddings/%
	cat $< | x_exp.py embeddings/$* > $@

ans/x_exp-s2p-tr-%-base.ans: ../data/data-files/sentence2phrase.train.input.tsv embeddings/%
	cat $< | x_exp.py embeddings/$* > $@

ans/%-scale.ans: ans/%.ans
	cat $< | scale.py 0 4 > $@

score/p2s-%.sc: ans/%.ans
	${SCORER} -c 0 ${GOLD_P2S} $< 

score/s2p-%.sc: ans/%.ans
	${SCORER} -c 0 ${GOLD_S2P} $< 

score/p2w-%.sc: ans/%.ans
	${SCORER} -c 0 ${GOLD_P2W} $< 

data/%.tok.tsv data/%.lem.tsv: corenlp-%.train
	-mkdir data
	corenlp-processor.py $<

export OMP_NUM_THREADS=10
TRAIN=../data/data-files/paragraph2sentence.train.input.tsv ../data/data-files/sentence2phrase.train.input.tsv ../data/data-files/phrase2word.train.input.tsv
FS_NSUB=100 # go until you have this many substitutes
FS_PSUB=1.0 # or this much cumulative probability
FS_OPTIONS=-n ${FS_NSUB} -p ${FS_PSUB}
train.sub.gz: ${TRAIN} # wc = 3000   67463  371790
	cat $^ | cut -f1,2 | tr '\t' '\n' | upenn_tokenizer.sed |\
	fastsubs-omp ${FS_OPTIONS} ${LM} | gzip > $@

### SCODE GLOBAL

tr-p2s.pairs.gz: data/paragraph2sentence.train.lem.tsv 
	sent_pairs.py <(cat $< | tr -cd "[:alpha:] [:space:]" | tr 'A-Z' 'a-z' |\
	remove-stop.py) | gzip > $@

tr-s2p.pairs.gz: data/sentence2phrase.train.lem.tsv 
	sent_pairs.py <(cat $< | tr -cd "[:alpha:] [:space:]" | tr 'A-Z' 'a-z' |\
	remove-stop.py) | gzip > $@

corpora.gz:
	corpora-sent.fetch.py | gzip > $@

enrichment.gz: corpora.gz
	zcat $< | tr -cd "[:alpha:] [:space:]" | tr 'A-Z' 'a-z' | remove-stop.py |\
	sent_enrich_pairs.py | gzip > $@

%.pairs.gz: tr-%.pairs.gz # enrichment.gz
	zcat $^ | gzip > $@

ans/sc_sent-%-tr.ans: %.scode.gz
	scode_sent_exp.py <(zcat $< | perl -ne 'print if s/^0://' | grep -P "^[LR]\d+" | cut -f1,3-) > $@

ans/sc_sent-%-tr.ans: %.scode.gz
	scode_sent_exp.py <(zcat $< | perl -ne 'print if s/^0://' | grep -P "^[LR]\d+" | cut -f1,3-) > $@

### Corpus Generation model experiments
gen-p2s-input: data/paragraph2sentence.train.lem.tsv 
	corp_gen_inp_create.py <(cat $< | tr -cd "[:alpha:] [:space:]" | tr 'A-Z' 'a-z' |\
	remove-stop.py) $@ > $@

clean-%: 
	-rm -rf ans/sc_sent-$*-tr.ans tr-$*.pairs.gz $*.pairs.gz $*.scode.gz

.PRECIOUS:
	rcv1.scode.gz
