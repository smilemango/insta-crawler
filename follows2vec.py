import sqlite3
import gensim
import codecs
import glob
import logging
import multiprocessing
import os
import pprint as pp
import re
import nltk
import gensim.models.word2vec as w2v
import sklearn.manifold
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns
import my_logger


my_logger.init_mylogger("follows2vec_logger","./log/follows2vec.log")

conn = sqlite3.connect('processed_data/insta_user_relations.sqlite3')
c = conn.cursor()

df = pd.read_sql_query("""
SELECT
    (SELECT username FROM users WHERE id = A.user_id) user_id,
    (SELECT username FROM users WHERE id = A.follow_id) follow_id
FROM relations A
--limit 10000 ;
""", conn)
trans =  df.groupby('user_id')['follow_id'].apply(lambda x: ",".join(x.astype(str)))
trans2 = trans.reset_index()['follow_id']

corpus = []
for x in trans2:
    corpus.append(x.split(','))

import gensim
import multiprocessing
import sklearn

#ONCE we have vectors
#step 3 - build model
#3 main tasks that vectors help with
#DISTANCE, SIMILARITY, RANKING

# Dimensionality of the resulting word vectors.
#more dimensions, more computationally expensive to train
#but also more accurate
#more dimensions = more generalized
num_features = 300
# Minimum word count threshold.
min_word_count = 150

# Number of threads to run in parallel.
#more workers, faster we train
num_workers = multiprocessing.cpu_count()

# Context window length.
context_size = 10

# Downsample setting for frequent words.
#0 - 1e-5 is good for this
downsampling = 1e-3

# Seed for the RNG, to make the results reproducible.
#random number generator
#deterministic, good for debugging
seed = 1


model = gensim.models.Word2Vec(
    sg=1,
    seed=seed,
    workers=num_workers,
    size=num_features,
    min_count=min_word_count,
    window=context_size,
    sample=downsampling
)


model.build_vocab(corpus)
print("Word2Vec vocabulary length:", len(model.wv.vocab))
model.train(corpus,total_examples=model.corpus_count, epochs=model.iter)


#my video - how to visualize a dataset easily
tsne = sklearn.manifold.TSNE(n_components=2, random_state=0)

all_word_vectors_matrix = model.wv.syn0
import pprint as pp
pp.pprint(model.wv.syn0[0])
all_word_vectors_matrix_2d = tsne.fit_transform(all_word_vectors_matrix)

points = pd.DataFrame(
    [
        (word, coords[0], coords[1])
        for word, coords in [
            (word, all_word_vectors_matrix_2d[model.wv.vocab[word].index])
            for word in model.wv.vocab
        ]
    ],
    columns=["word", "x", "y"]
)


pp.pprint(points.head(10))


import seaborn as sns
sns.set_context("poster")

from sklearn.manifold import TSNE
from mpl_toolkits.mplot3d import Axes3D
from matplotlib import font_manager, rc
import matplotlib.pyplot as plt
import pylab

font_name = font_manager.FontProperties(fname="c:/Windows/Fonts/malgun.ttf").get_name()
rc('font', family=font_name)


ax = points.plot.scatter("x", "y", s=10, figsize=(20, 12))
for i, point in points.iterrows():
    ax.text(point.x + 0.0001, point.y + 0, point.word, fontsize=11)

# print(model.most_similar(positive=['lovelymrsyi']))
#
# for value in points.values:
#     if value[0] =='lovelymrsyi':
#         print(value)


plt.show()