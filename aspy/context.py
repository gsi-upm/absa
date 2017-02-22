import json
import sys
from dparpy.graph import GraphMatrix
from dparpy.dparpy import extract_dependencies
from lxml import etree
import os
import string

noise = set(string.punctuation)-set("'/$+")  # > and < are removed also
noise = {ord(c): None for c in noise}

def identifyTargets(naf):
    root = etree.fromstring(naf)
    targets = []
    terms = []
    words = []
    entity = [entity for entity in root.findall(".//entity")]
    for item in entity:
        targets.append(item.findall(".//target"))
    for item in targets:
        terms.append([terms.find(".*/target").get("id") for terms in root.findall(".//term") for target in item if terms.get("id") == target.get("id")])
    for item in terms:
        words.append([words.text for words in root.findall(".//wf") for term in item if words.get("id") == term])
    return words

def normalize_text(t):
    t = t.translate(noise)
    return t
def findContext(deps,naf):

    dep = deps['sentences'][0]
    g = GraphMatrix(dep)
    contexts = []
    features_ixa = identifyTargets(naf)
    #Aquí realizamos los cambios pertinentes en las targets de IXA para que coincidan con el parser de stanford.
    for items in features_ixa:
        for item in items:
            if "'" in item:
                items[items.index(item)-1] += item
                items.remove(item)
            if item.endswith('/'):
                items[items.index(item) - 1] += item
                items.remove(item)
            if item.startswith('$'):
                items[items.index(item) + 1] = item + items[items.index(item) + 1]
                items.remove(item)
    for feature in g.features:
        response = extract_dependencies(target_feature=feature, deps=dep, verbose=False,threshold=1, graph=g)
        context = sorted(list(response), key=lambda k: int(k.split('-')[-1]))
        if (len(feature.split('-')) > 2) and (not feature.replace(feature.split('-')[-1],'')[0:-1].endswith('-')):
            noise = set(string.punctuation) - set("'/-")  # > and < are removed also
            noise = {ord(c): None for c in noise}
            feature = feature.replace(feature.split('-')[-1],'')[0:-1]
            feature = normalize_text(feature)
            noise = set(string.punctuation) - set("'/")  # > and < are removed also
            noise = {ord(c): None for c in noise}
        else:
            feature = normalize_text(feature.split('-')[0])


        f_ixa = [feats for feats in features_ixa if (feature in feats)]
        if len(f_ixa[0]) > 1:
            if feature == f_ixa[0][0]:
                contexts.append({'feature': feature, 'context': context})

            else:
                first_word = [element for element in contexts if f_ixa[0][0] in element['feature']]
                first_word[0]['feature'] += ' ' + feature
                context_union = set(first_word[0]['context']) | set(context)
                first_word[0]['context'] = sorted(list(context_union), key=lambda k: int(k.split('-')[-1]))
        else:
            contexts.append({'feature': feature, 'context': context})

    for element in contexts:
        element['context'] = [item.split('-')[0] for item in element['context']]
    return contexts



