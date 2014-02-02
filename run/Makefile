SHELL := /bin/bash

.SECONDARY:

### PATH
SRILM_PATH=/opt/srilm/bin/i686-m64
CORE_NLP_PATH=../../tools/src/stanford-corenlp

export PATH:=.:../../tools/bin/:${SRILM_PATH}:${PATH}

SEED=1
CPU=8

LM=enw.lm.gz

SCORER= java -jar ../data/evaluation/task-3-scorer.jar

bin:
	cd ../bin; make

enw.lm.gz:
	ln -s /scratch/1/myatbaz/upos_new/run/enw_ukvac2/enw.lm.gz

SC_OPTIONS=-s ${SEED} -v
%.scode.gz: %.pairs.gz
	zcat $< | scode ${SC_OPTIONS} | gzip > $@

# Stanford CoreNLP is used for tokenization, tagging, and dependency parsing
CORE_NLP=java -mx8g -cp "${CORE_NLP_PATH}/*" edu.stanford.nlp.pipeline.StanfordCoreNLP 
ANNOTATORS=-annotators "tokenize, ssplit, pos, lemma, parse"
CNLP_OPTIONS=${ANNOTATORS} -replaceExtension -threads ${CPU} 
corenlp-%: ../data/data-files/%.input.tsv
	-rm -rf docs; mkdir docs
	cat $< | cut -f1,2 | awk 'BEGIN{i=1}{printf("%s\n", $$0) > "docs/"i++".txt"}'
	${CORE_NLP} ${CNLP_OPTIONS} -outputDirectory $@ -file docs/ 


### BASELINE ###
ans/ji-baseline-%.ans: ../data/data-files/%.input.tsv
	cat $< | ji-baseline.py > $@

#SVEC=rcv1.scode.gz
SVEC=wsj.scode.gz
GOLD=../data/keys/paragraph2sentence.train.gs.tsv

ans/x_exp-%-lemma.ans: %.tsv
	cat $< | x_exp.py ${SVEC} > $@

ans/x_exp-%-base.ans: ../data/data-files/%.input.tsv ${SVEC}
	cat $< | x_exp.py ${SVEC} > $@

ans/%-scale.ans: ans/%.ans
	cat $< | scale.py 0 4 > $@

score/%.sc: ans/%.ans
	${SCORER} -c 0 ${GOLD} $< 

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

.PRECIOUS:
	rcv1.scode.gz
