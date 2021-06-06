# -*- coding: utf-8 -*-
""" 

Text clustering classification  

Used to created the analysi and define labels for the dataset.

Retrieve from:
    https://nlpforhackers.io/recipe-text-clustering/

"""

import collections
from sklearn.cluster import KMeans
from sklearn.feature_extraction.text import TfidfVectorizer
from nltk.corpus import stopwords

def cluster_texts(texts, clusters=3):
    """ Transform texts to Tf-Idf coordinates and cluster texts using K-Means """
    vectorizer = TfidfVectorizer(# tokenizer=texts,
                                # max_df=0.5,
                                # min_df=0.1,
                                 lowercase=True)
 
    tfidf_model = vectorizer.fit_transform(texts)
    km_model = KMeans(n_clusters=clusters)
    km_model.fit(tfidf_model)
 
    clustering = collections.defaultdict(list)
 
    for idx, label in enumerate(km_model.labels_):
        clustering[label].append(idx)
 
    return clustering
 
"""

#TF-IDF vectorizer
stop_words = set(stopwords.words("english"))
tfv = TfidfVectorizer(stop_words = stop_words, ngram_range = (1,1))
#transform
vec_text = tfv.fit_transform(text)
#returns a list of words.
words = tfv.get_feature_names()

print(words)

#cluster = cluster_texts(text)
"""


