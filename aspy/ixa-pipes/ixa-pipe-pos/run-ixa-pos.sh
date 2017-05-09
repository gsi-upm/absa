cd /ixa-pipe-pos
mvn clean package

java -jar /ixa-pipe-pos/target/ixa-pipe-pos-1.5.1-exec.jar server -p 2040 -l en -m /data/morph-models-1.5.0/en/en-pos-perceptron-autodict01-conll09.bin -lm /data/morph-models-1.5.0/en/en-lemma-perceptron-conll09.bin 
