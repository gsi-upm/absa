#!/bin/sh
cd /ixa-pipe-tok
mvn clean package

java -jar /ixa-pipe-tok/target/ixa-pipe-tok-1.8.5-exec.jar server -p 2030 -n default -l en --inputkaf 
 
