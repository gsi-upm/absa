#!/usr/bin/env python

import json
import sys
import numpy as np
import pandas as pd
#from textblob import Word
from scipy import sparse


class StanfordNLP:
    def __init__(self, port_number=8080):
        self.server = jsonrpclib.Server("http://localhost:%d" % port_number)

    def parse(self, text):
        return json.loads(self.server.parse(text))


class GraphMatrix:
    def __init__(self, stanford_parsed=None):
        self._excluded_dependencies = ['ROOT'] # , 'dep'] # As explained in literature
        self._stanford_parsed = stanford_parsed
        self._sent = self._get_sentence_features()
        self.sentence = self._sent['sentence']
        self.features = self._sent['features']
        self.len_sentence = len(self.sentence)
        self.matrix = self._create_matrix()

    def _singularize_word(self, word):
        return Word(word).singularize()

    def _word_index(self, word):
        return int(word.split('-')[-1]) - 1

    def _get_sentence_features(self):
        sentence = list()
        features = list()

        for token in self._stanford_parsed['tokens']:
            word = token['word']
            index = token['index']
            word_position = '{}-{}'.format(word, str(index))
            sentence.append(word_position)
            if not token.get('feature') is None and token.get('feature'):
                features.append(word_position)


        sentence_data = {'sentence': sentence, 'features': features}
        return sentence_data

    def _create_matrix(self):
        ind_dep = self._stanford_parsed['collapsed-dependencies']

        # Create matrix filled with inf
        matrix = np.full([self.len_sentence,self.len_sentence], np.inf)
        # Set the diagonal to all zeros: dist(wi,wi) = 0
        for i, row in enumerate(matrix):
            row[i] = 0

        # Set the elements directly connected to 1
        for dep in ind_dep:
            if dep['dep'] in self._excluded_dependencies:
                continue

            # word1 = dep[1].split('-') # wordi[0] -> the word; wordi[1] -> the index
            # word1 = word1[-1]
            # word2 = dep[2].split('-')
            # word2 = word2[-1]

            governor = dep['governor'] - 1
            dependent = dep['dependent'] - 1

            matrix[governor][dependent] = 1 # Matrix is symmetric
            matrix[dependent][governor] = 1 # Matrix is symmetric

        shortest_paths_matrix = sparse.csgraph.dijkstra(matrix)
        return shortest_paths_matrix

    # Too old. Did not use pandas
    def _print_matrix(self):
        print("GraphMatrix:", ' '.join(self.sentence))
        line = '\t\t| '
        for word in self.sentence:
            if word in self.features:
                word = '['+str(word)+']'
                line += str(word)+'\t'

        sys.stdout.write(line+'\n')
        sys.stdout.write('-'*16+'+'+'--'*len(line)+'\n')

        for i, word in enumerate(self.sentence):
            if word in self.features:
                word = '['+str(word)+']'
                line = str(word) + '\t\t| '
                for num in self.matrix[i]:
                    if num == np.inf:
                        num = 'inf'
                    else:
                        num = int(num)
                        line += str(num) + '\t'
                        line += '\n'
                        sys.stdout.write(line)
                        sys.stdout.write('\n')
                        sys.stdout.flush()

    def print_matrix(self):
        matrix = pd.DataFrame(columns=self.sentence,
                              index=range(self.matrix.shape[0]),
                              data=self.matrix)
        print(matrix)

    # This method will be deprecated
    def _words_distance(self, index1, index2):
        indx1, indx2 = self.sentence.index(index1), self.sentence.index(index2)
        return self.matrix[indx1][indx2]

    def indexes_distance(self, index1, index2):
        return self.matrix[index1][index2]

    def words_distance(self, w1, w2):
        indx1, indx2 = self._word_index(w1), self._word_index(w2)
        return self.matrix[indx1, indx2]
