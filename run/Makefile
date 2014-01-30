SHELL := /bin/bash
.SECONDARY:

### PATH
SRILM_PATH=/opt/srilm/bin/i686-m64
CORE_NLP_PATH=/scratch/1/obaskaya/tools/src/stanford-corenlp

export PATH:=.:/scratch/1/obaskaya/tools/bin/:${SRILM_PATH}:${PATH}

SEED=1
CPU=8

bin:
	cd ../bin; make

SC_OPTIONS=-s ${SEED} -v
%.scode.gz: %.pairs.gz
	zcat $< | scode ${SC_OPTIONS} | gzip > $@

# Stanford CoreNLP is used for tokenization, tagging, and dependency parsing
CORE_NLP=java -mx8g -cp "${CORE_NLP_PATH}/*" edu.stanford.nlp.pipeline.StanfordCoreNLP 
ANNOTATORS=-annotators "tokenize, ssplit, pos, parse"
CNLP_OPTIONS=${ANNOTATORS} -replaceExtension -threads ${CPU} -outputDirectory .
%.trial.input.xml: ../data/trial-data/%.trial.input.txt
	touch $@
	${CORE_NLP} ${CNLP_OPTIONS} -file $<

%.train.input.xml: ../data/train-data/%.train.input.txt
	touch $@
	${CORE_NLP} ${CNLP_OPTIONS} -file $<

TRIAL="../data/trial-data/paragraph2sentence.trial.input.txt"
x_exp: rcv1.scode.gz
	x_exp.py $< ${TRIAL}



.PRECIOUS:
	rcv1.scode.gz
