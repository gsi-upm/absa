import socket
from lxml import etree
import requests
import json
import context
import os
import string
from os import path
import aspect
import time
from senpy.plugins import SentimentPlugin, SenpyPlugin
from senpy.models import Results, Entry, Sentiment

class AspyPlugin(SentimentPlugin):

    def analyse(self, **params):

        intext = params.get("input", None)

        # Review input
        naf = b'<NAF xml:lang="en" version="v1.naf">\n<raw><![CDATA['+bytes(intext,'utf-8')+b']]>\n  </raw> \n</NAF>\n'
        BUFF_SIZE = 262144
        TIME_SLEEP = 0.25
        # ixa pipe tok
        tok = b''
        while not tok.endswith(b'</NAF>\n'):
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            s.connect(("localhost", 2030))
            s.send(naf)
            tok = s.recv(BUFF_SIZE)
            time.sleep(TIME_SLEEP)

        # ixa pipe pos
        pos = b''
        while not pos.endswith(b'</NAF>\n'):
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            s.connect(("localhost", 2040))
            s.send(tok)
            pos = s.recv(BUFF_SIZE)
            time.sleep(TIME_SLEEP)

        # ixa pipe nerc
        naf = b''
        while not naf.endswith(b'</NAF>\n'):
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            s.connect(("localhost", 2060))
            s.send(pos)
            naf = s.recv(BUFF_SIZE)
            time.sleep(TIME_SLEEP)
        # CoreNLPParser
        parsed = ""
        r = requests.post(
            'http://192.168.99.100:9000/?properties={"tokenize.whitespace":"true","ssplit.eolonly":"true","annotators":"tokenize,ssplit,pos,depparse","outputFormat":"json"}',
            data=intext)
        parsed = json.loads(r.text)

        # CoreNLPParser + feature
        root = etree.fromstring(naf)
        targets = [target.get("id") for target in root.findall(".//entity//target")]
        terms = [terms.find(".*/target").get("id") for terms in root.findall(".//term") for target in targets if
                 terms.get("id") == target]
        features = [words for words in root.findall(".//wf") for term in terms if words.get("id") == term]
        for element in [tokens for tokens in parsed['sentences'][0]['tokens'] for feature in features if
                        tokens['characterOffsetBegin'] == int(feature.get("offset"))]:
            element['feature'] = True

        # dparpy
        contexts = context.findContext(parsed, naf)

        # Sematch
        a = aspect.Aspect()
        for asp in contexts:
            contexts[contexts.index(asp)]['topic'] = a.knn_classify(asp['feature'])

        #SentiText
        for aspct in contexts:
            r = requests.get('http://127.0.0.1:8080/api/?algo=sentiText&i=' + " ".join(aspct['context']))
            response_sentitext = r.content.decode('utf-8')
            response_json = json.loads(response_sentitext)
            aspct['polarity'] = response_json['entries'][0]['sentiments'][0]['marl:hasPolarity']
            aspct['polarityValue'] = response_json['entries'][0]['sentiments'][0]['marl:polarityValue']
        #Senpy Response
        response = Results()
        entry = Entry(id="Entry0", nif__isString=intext)
        entry.sentiments = []
        for aspec in contexts:
            opinion = Sentiment(id="Aspect"+str(contexts.index(aspec)),nif__anchorOf = " ".join(aspec['context']))
            opinion.marl__hasPolarity = aspec['polarity']
            opinion.marl__describesObject = aspec['feature']
            opinion.marl__polarityValue = aspec['polarityValue']
            opinion.marl__describesObjectFeature = aspec['topic']
            topic = aspec['topic'][0].upper() + aspec['topic'][1:]
            if aspec['topic'] == "drinks":
                opinion.marl__forDomain = "http://dbpedia.org/page/Drink"
            elif aspec['topic'] == "ambience":
                opinion.marl__forDomain = "http://dbpedia.org/page/Atmosphere"
            else:
                opinion.marl__forDomain = "http://dbpedia.org/page/" + topic
            opinion["prov:wasGeneratedBy"] = self.id
            entry.sentiments.append(opinion)
        response.entries.append(entry)
        return response
