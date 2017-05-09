cd /ixa-pipe-nerc
mvn clean package

java -jar /ixa-pipe-nerc/target/ixa-pipe-nerc-1.6.1-exec.jar server -l en -p 2060 -m /data/ote-models-1.5.4/ote-2015-restaurants.bin 
