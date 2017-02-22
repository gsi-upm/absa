__author__ = 'oaraque'

import string
from dparpy.clustering import DependencyCluster, DependencyClusterSet
from dparpy.graph import StanfordNLP, GraphMatrix
from pprint import pprint

# def to_unicode(obj, encoding='utf-8'):
#     if isinstance(obj, basestring):
#         if not isinstance(obj, unicode):
#             obj = unicode(obj, encoding)
#     return obj

def initialize_clusters(graph=None):
    """
    Initializes the n clusters and inserts them into a cluster set.
    There is a cluster for each feature.
    :param graph: Instance of the GraphMatrix class that represents the graph of the sentence.
    :return: An instance of the DependencyClusterSet class with all the clusters initialized
    """
    features = graph.features
    dependency_cluster_set = DependencyClusterSet(graph=graph)
    for feature in features:
        dependency_cluster = DependencyCluster(clusterhead=feature, graph=graph)
        dependency_cluster_set.insert_cluster(dependency_cluster)
    return dependency_cluster_set

def preprocess(text=None):
    punctuation = set('!"$%&\'()*+,-./:;<=>?[\\]^_`{|}~')
    # Filter number from text, as they provoke decoding errors in the Stanford Parser
    text = u''.join(c if c not in map(str,range(0,10)) else u'' for c in text)
    # Remove punctuation from text as it does not help the analysis
    text = u''.join(c if c not in punctuation else u'' for c in text)

    ## Lower the words and singularize them
    text = u' '.join(w.lower() for w in text.split())
    ##
    return text

def extract_dependencies(text=None, threshold=3, target_feature=None,
                         deps=None, graph=None, verbose=False):
    result = deps

    if verbose:
        print("Result from dependency parsing:")
        pprint(result)
        print('\n')

    if graph is None:
        graph = GraphMatrix(result)

    if verbose:
        graph.print_matrix()
    dcs = initialize_clusters(graph=graph)
    dcs.assign_words_to_clusters()
    if verbose and target_feature is None:
        print('-'*10, "Clusters previous merging", '-'*10)
        dcs.show_clusters()
        print('-'*47)
    if not target_feature is None:
        dcs.merge_clusters(threshold=threshold, target_feature=target_feature)
        if verbose:
            dcs.show_clusters()
        return dcs.get_cluster_words(clusterhead=target_feature)
    else:
        clstr_set = []
        for cluster in dcs.cluster_set:
            clstr_set.append({'clusterhead': cluster, 'cluster': dcs.get_cluster_words(clusterhead=cluster)})
        return clstr_set
    #list_nou [cluster for cluster in dcs.cluster_set]
