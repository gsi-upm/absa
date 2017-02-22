__author__ = 'oaraque'

import math
import numpy as np
from collections import defaultdict
from pprint import pprint
from dparpy.graph import GraphMatrix

class DependencyCluster(object):
    """
    Class representing the cluster that are created when dependency parsing.
    """

    def __init__(self, clusterhead=None, graph=None, *args, **kwargs):
        self.clusterhead = clusterhead
        self.assigned_words = defaultdict(str)
        if isinstance(graph, GraphMatrix):
            self.graph = graph

    def assign_word(self, word=None, distance=None):
        if isinstance(word, str):
            if isinstance(distance, int):
            #distance_to_cluster = self.graph.words_distance(self.clusterhead, word)
                self.assigned_words[word] = int(distance)


class DependencyClusterSet(object):
    """
    Class representing the sets of clusters that are initialized inside the dependency parsing algorithm
    """

    def __init__(self, graph=None):
        self.cluster_set = defaultdict(DependencyCluster)
        if isinstance(graph, GraphMatrix):
            self.graph = graph

    def insert_cluster(self, dep_cluster):
        """
        Inserts a DependencyCluster instance into the set of DependencyClusterSet class set
        :param dep_cluster: instance of the DependencyCluster class
        :return:
        """
        if isinstance(dep_cluster, DependencyCluster):
            clusterhead = str(dep_cluster.clusterhead)
            self.cluster_set[clusterhead] = dep_cluster

    def assign_words_to_clusters(self):
        """
        Assign each word of the sentence to the corresponding cluster. The criteria used is the minimum distance to
        the clusterhead in terms of the graph of the sentence. In case the distance in inf (no connection), the word in
        assigned to no cluster. In the case in which a word has the same minimum distance to two or more features,
        the more close feature in terms of sentence distance (distance in the writing of the sentence) is selected.
        :return: None
        """
        # Dict created for accessing the features indexes on the graph matrix
        features_indexes = defaultdict(int)
        for feature in self.graph.features:
            features_indexes[feature] = self.graph.sentence.index(feature)

        for index, word in enumerate(self.graph.matrix):
            assigned_word = self.graph.sentence[index]
            distances = {}
            for feature in features_indexes:
                distances[feature] = word[features_indexes[feature]]
            ####
            #if distances == {}:
            #    return
            ####
            min_distance_feature = min(distances, key=distances.get)  # Get the key with the minimun distance
            min_distance = distances[min_distance_feature]  # The min distance value

            # If the minimum distance is infinite (no connection between the words), do not assign the word
            if min_distance == np.inf:
                continue

            # If there is several features with the same minimum distance, assign to the
            # more close to the word
            n_coincidences = 0
            for feature, distance in distances.items():
                if distance == min_distance:
                    n_coincidences += 1
            if n_coincidences > 1:
                sentence_distances = {}
                for feature in self.graph.features:
                    sentence_distances[feature] = math.fabs(self.graph.sentence.index(assigned_word) \
                                                            - self.graph.sentence.index(feature))
                min_sentence_distance_feature = min(sentence_distances, key=sentence_distances.get)
                min_distance_feature = min_sentence_distance_feature

            # Assign the word to the corresponding cluster that is into the cluster set
            self.cluster_set[min_distance_feature].assign_word(word=str(assigned_word), distance=int(min_distance))

    def merge_clusters(self, threshold=None, target_feature=None):
        """
        Merge any cluster with the cluster whose clusterhead is the target feature if the distance between the
        clusterheads is lower than the threshold.
        :param threshold: If the distance between two clusterheads is lower than this parameter, the clusters are merged
        :param target_feature: The target feature. The clusters, if any, will be merged with it
        :return: None
        """
        threshold, target_feature = int(threshold), str(target_feature)
        cluster_set = self.cluster_set.copy()
        for clusterhead in cluster_set.keys():
            if clusterhead == target_feature:
                continue
            distance = self.graph.words_distance(target_feature, clusterhead)
            if distance < threshold:
                self.cluster_set[target_feature].assigned_words.update(self.cluster_set[clusterhead].assigned_words)
                del self.cluster_set[clusterhead]

    def show_clusters(self):
        """
        Shows the words associated with each cluster.
        :return: None
        """
        for cluster in self.cluster_set:
            print('Set of words of feature',
                  self.cluster_set[cluster].clusterhead)
            pprint(self.cluster_set[cluster].assigned_words.keys())

    def get_cluster_words(self, clusterhead=None):
        """
        Return the set of words of a cluster with the clusterhead passed as a parameter
        :return: List of words associated with the cluster
        """
        return self.cluster_set[clusterhead].assigned_words.keys()
