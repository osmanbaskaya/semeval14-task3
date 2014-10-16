SHELL := /bin/bash

.SECONDARY:

### PATH
SRILM_PATH=/ai/opt/srilm/bin/i686-m64
CORE_NLP_PATH=../../tools/src/stanford-corenlp

export PATH:=${PATH}:.:../../tools/bin:${SRILM_PATH}

SEED=1
CPU=2
LM=enw.lm.gz
SCORER= java -jar ../data/evaluation/task-3-scorer.jar

bin:
	cd ../bin; make

enw.lm.gz:
	ln -s /scratch/1/myatbaz/upos_new/run/enw_ukvac2/enw.lm.gz

SC_OPTIONS=-s ${SEED} -v -d 100
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

# FIXME: separate those targets so that dependency will work.
# call example: make data/sentence2phrase.lem.tsv DATASET_TYPE=test
data/%.tok.tsv data/%.lem.tsv: corenlp-%.${DATASET_TYPE}
	-mkdir data
	python corenlp-processor.py $<

### BASELINE ###
ans/ji-baseline-%.ans: ../data/data-files/%.input.tsv
	cat $< | python ji-baseline.py > $@

# WN-based baselines
ans/wn-train-%-sentence2phrase.ans: data/sentence2phrase.train.lem.tsv
	cat $< | python data-preprocess.py -l | python wn-baseline.py $* > $@
 
ans/wn-train-%-paragraph2sentence.ans: data/paragraph2sentence.train.lem.tsv
	cat $< | python data-preprocess.py -l | python wn-baseline.py $* > $@

ans/wn-test-%-sentence2phrase.ans: data/sentence2phrase.test.lem.tsv
	cat $< | python data-preprocess.py -l | python wn-baseline.py $* > $@
 
ans/wn-test-%-paragraph2sentence.ans: data/paragraph2sentence.test.lem.tsv
	cat $< | python data-preprocess.py -l | python wn-baseline.py $* > $@

### EMBEDDING EXP ###
ans/x_exp-p2s-tr-%-base.ans: ../data/data-files/paragraph2sentence.train.input.tsv embeddings/%
	cat $< | python x_exp.py embeddings/$* > $@

ans/x_exp-s2p-tr-%-base.ans: ../data/data-files/sentence2phrase.train.input.tsv embeddings/%
	cat $< | python x_exp.py embeddings/$* > $@

ans/%-scale.ans: ans/%.ans
	cat $< | python scale.py 0 4 > $@

# call example: make score/p2s-SYSTEMNAME.sc DATASET_TYPE=test
# call example: make score/p2s-SYSTEMNAME.sc DATASET_TYPE=train
score/p2s-%.sc: ../data/keys/paragraph2sentence.${DATASET_TYPE}.gs.tsv ans/%.ans
	${SCORER} -c 0 $^

score/s2p-%.sc: ../data/keys/sentence2phrase.${DATASET_TYPE}.gs.tsv ans/%.ans
	${SCORER} -c 0 $^

score/p2w-%.sc: ../data/keys/phrase2word.${DATASET_TYPE}.gs.tsv ans/%.ans
	${SCORER} -c 0 $^ 

#data/%.tok.tsv data/%.lem.tsv: corenlp-%.train
	#-mkdir data
	#corenlp-processor.py $<

data/%.tok.tsv data/%.lem.tsv: corenlp-%.test
	-mkdir data
	python corenlp-processor.py $<

export OMP_NUM_THREADS=15
TRAIN=../data/data-files/paragraph2sentence.train.input.tsv ../data/data-files/sentence2phrase.train.input.tsv ../data/data-files/phrase2word.train.input.tsv
FS_NSUB=100 # go until you have this many substitutes
FS_PSUB=1.0 # or this much cumulative probability
FS_OPTIONS=-n ${FS_NSUB} -p ${FS_PSUB}
train.sub.gz: ${TRAIN} # wc = 3000   67463  371790
	cat $^ | cut -f1,2 | tr '\t' '\n' | upenn_tokenizer.sed |\
	fastsubs-omp ${FS_OPTIONS} ${LM} | gzip > $@

train-%.sub: ../data/data-files/%.train.input.tsv
	cat $< | cut -f${FIELD} | upenn_tokenizer.sed |\
	fastsubs-omp ${FS_OPTIONS} ${LM} | gzip > $@.f${FIELD}.gz

test-%.sub: ../data/data-files/%.test.input.tsv
	cat $< | cut -f${FIELD} | upenn_tokenizer.sed |\
	fastsubs-omp ${FS_OPTIONS} ${LM} | gzip > $@.f${FIELD}.gz

### SCODE GLOBAL

%-p2s.pairs.gz: data/paragraph2sentence.%.lem.tsv 
	python sent_pairs.py <(cat $< | tr -cd "[:alpha:] [:space:]" | tr 'A-Z' 'a-z' |\
	python remove-stop.py) | gzip > $@

%-s2p.pairs.gz: data/sentence2phrase.%.lem.tsv 
	python sent_pairs.py <(cat $< | tr -cd "[:alpha:] [:space:]" | tr 'A-Z' 'a-z' |\
	python remove-stop.py) | gzip > $@

%-p2w.pairs.gz: data/phrase2word.%.lem.tsv 
	python sent_pairs.py <(cat $< | tr -cd "[:alpha:] [:space:]" | tr 'A-Z' 'a-z' |\
	python remove-stop.py) | gzip > $@

corpora.gz:
	python corpora-sent.fetch.py | gzip > $@

enrichment.gz: corpora.gz
	zcat $< | tr -cd "[:alpha:] [:space:]" | tr 'A-Z' 'a-z' | python remove-stop.py |\
	python sent_enrich_pairs.py | gzip > $@

%.pairs.gz: tr-%.pairs.gz # enrichment.gz
	zcat $^ | gzip > $@

%-sub-p2s.pairs.gz: %-paragraph2sentence.sub.f1.gz %-paragraph2sentence.sub.f2.gz
	zcat $< | python wordsub_task3.py L 100 1 > $@.tmp
	zcat $*-paragraph2sentence.sub.f2.gz | python wordsub_task3.py R 100 1 >> $@.tmp
	cat $@.tmp | gzip > $@
	rm $@.tmp

%-sub-s2p.pairs.gz: %-sentence2phrase.sub.f1.gz %-sentence2phrase.sub.f2.gz
	zcat $< | python wordsub_task3.py L 100 1 > $@.tmp
	zcat $*-sentence2phrase.sub.f2.gz | python wordsub_task3.py R 100 1 >> $@.tmp
	cat $@.tmp | gzip > $@
	rm $@.tmp

test-%-s1.pairs.gz: train-%.pairs.gz test-%.pairs.gz
	zcat $< | sed -e 's|^L|T|g' -e 's|^R|K|g' | gzip > $@.tmp
	zcat test-$*.pairs.gz $@.tmp | gzip > $@
	rm $@.tmp

test-%-s2.pairs.gz: train-sub-%.pairs.gz test-sub-%.pairs.gz
	zcat $< | sed -e 's|^L|T|g' -e 's|^R|K|g' | gzip > $@.tmp
	zcat test-$*.pairs.gz $@.tmp | gzip > $@
	rm $@.tmp

ans/test-%-s1.ans: test-%-s1.scode.gz
	python scode_sent_exp.py <(zcat $< | perl -ne 'print if s/^0://' | grep -P "^[LR]\d+" | cut -f1,3-) > $@

ans/test-%-s2.ans: test-%-s2.scode.gz
	python scode_sent_exp.py <(zcat $< | perl -ne 'print if s/^0://' | grep -P "^[LR]\d+" | cut -f1,3-) > $@

ans/train-sc_sent-%.ans: train-%.scode.gz
	python scode_sent_exp.py <(zcat $< | perl -ne 'print if s/^0://' | grep -P "^[LR]\d+" | cut -f1,3-) > $@

ans/train-sc_sub-%.ans: train-sub-%.scode.gz
	python scode_sent_exp.py <(zcat $< | perl -ne 'print if s/^0://' | grep -P "^[LR]\d+" | cut -f1,3-) > $@

### Corpus Generation model experiments
gen-p2s-input: data/paragraph2sentence.train.lem.tsv 
	python corp_gen_inp_create.py <(cat $< | tr -cd "[:alpha:] [:space:]" | tr 'A-Z' 'a-z' |\
	python remove-stop.py) $@ > $@

gen-p2s-input-uniq: gen-p2s-input
	cat $< | sort | uniq > $@

gen-p2s-prob.gz: rcv1.sub.gz all.stem gen-p2s-input-uniq
	zcat $< | head -1000000 | python features.py all.stem gen-p2s-input-uniq |\
	uniq2pairs.gz gen-p2s-input | gzip > $@

clean-%: 
	-rm -rf ans/sc_sent-$*-tr.ans tr-$*.pairs.gz $*.pairs.gz $*.scode.gz

sub-clean-%:
	-rm -rf train-sub-$*.scode.gz ans/sc_sub-train-sub-$*.ans

.PRECIOUS:
	rcv1.scode.gz
