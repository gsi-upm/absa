#!/bin/sh
java -jar /ixa-pipe-tok/target/ixa-pipe-tok-1.8.4.jar server -p 2030 -n default -l en --inputkaf
java -jar /ixa-pipe-pos/target/ixa-pipe-pos-1.5.1.jar server -p 2040 -l en -m /data/morph-models-1.5.0/en/en-pos-perceptron-autodict01-conll09.bin -lm /data/morph-models-1.5.0/en/en-lemma-perceptron-conll09.bin
java -jar /ixa-pipe-nerc/target/ixa-pipe-nerc-1.5.4.jar server -l en -p 2060 -m /data/ote-models-1.5.4/ote-2015-restaurants.bin
 
