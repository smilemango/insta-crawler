import sqlite3
import logging
import pprint as pp
import matplotlib.pyplot as plt
import pandas as pd
import os, sys
import gensim
import multiprocessing
import sklearn
from sklearn.manifold import TSNE
from matplotlib import font_manager, rc
from matplotlib.widgets import RadioButtons

import my_logger

# ONCE we have vectors
# step 3 - build model
# 3 main tasks that vectors help with
# DISTANCE, SIMILARITY, RANKING

# Dimensionality of the resulting word vectors.
# more dimensions, more computationally expensive to train
# but also more accurate
# more dimensions = more generalized
num_features = 500
# Minimum word count threshold.
min_word_count = 100

# Number of threads to run in parallel.
# more workers, faster we train
num_workers = multiprocessing.cpu_count()

# Context window length.
context_size = 20

# Downsample setting for frequent words.
# 0 - 1e-5 is good for this
downsampling = 1e-3

# Seed for the RNG, to make the results reproducible.
# random number generator
# deterministic, good for debugging
seed = 1

sg = 0

SAVED_FILE_PATH = "./vector/follows2vec_%d_%d_%d.w2v" % ( num_features, context_size, sg )

logger = my_logger.init_mylogger("follows2vec_logger","./log/follows2vec.log")


model = None

if os.path.isfile(SAVED_FILE_PATH):
    logger.info("Vector data already exists.")
    logger.info("Load data...")
    model = gensim.models.Word2Vec.load(SAVED_FILE_PATH)

else :
    logger.info("Vector data does not exist.")
    conn = sqlite3.connect('processed_data/insta_user_relations.sqlite3')
    c = conn.cursor()

    logger.info("Loading Database.")
    df = pd.read_sql_query("""
    SELECT
        (SELECT username FROM users WHERE id = A.user_id) user_id,
        (SELECT username FROM users WHERE id = A.follow_id) follow_id
    FROM relations A
    --limit 100 ;
    """, conn)
    logger.info("Database loading completed.")
    logger.info("Data transforming... Group By 'USER_ID'")
    trans =  df.groupby('user_id')['follow_id'].apply(lambda x: ",".join(x.astype(str)))
    trans2 = trans.reset_index()['follow_id']

    corpus = []
    for x in trans2:
        corpus.append(x.split(','))

    logger.info("Data preprocessing completed.")

    model = gensim.models.Word2Vec(
        sg=sg,
        seed=seed,
        workers=num_workers,
        size=num_features,
        min_count=min_word_count,
        window=context_size,
        sample=downsampling
    )

    logger.info("Building vocablary.")
    model.build_vocab(corpus)
    logger.info("Word2Vec vocabulary length : %d", len(model.wv.vocab))
    logger.info("Traing...")
    model.train(corpus,total_examples=model.corpus_count, epochs=model.iter)
    logger.info("Traing completed.")

    model.save(SAVED_FILE_PATH)


#my video - how to visualize a dataset easily
tsne = sklearn.manifold.TSNE(n_components=2, random_state=0)
all_word_vectors_matrix = model.wv.syn0
#pp.pprint(model.wv.syn0[0])

logging.info("Vector to 2d matrix.")
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


# .---------------------.----------.
# | System              | Value    |
# |---------------------|----------|
# | Linux (2.x and 3.x) | linux2   |
# | Windows             | win32    |
# | Windows/Cygwin      | cygwin   |
# | Mac OS X            | darwin   |
# | OS/2                | os2      |
# | OS/2 EMX            | os2emx   |
# | RiscOS              | riscos   |
# | AtheOS              | atheos   |
# | FreeBSD 7           | freebsd7 |
# | FreeBSD 8           | freebsd8 |
# '---------------------'----------'

if sys.platform == 'win32':
    font_name = font_manager.FontProperties(fname="c:/Windows/Fonts/malgun.ttf").get_name()
    rc('font', family=font_name)
elif sys.platform == 'darwin':
    rc('font', family="AppleGothic")

plt.rcParams['axes.unicode_minus'] = False

ax = points.plot.scatter("x", "y", s=10, figsize=(20, 12))
text_labels = []
for i, point in points.iterrows():
    t= ax.text(point.x + 0.0001, point.y, point.word, fontsize=11, url="http://www.instagram.com/" + point.word)
    text_labels.append( t)


# the left side of the subplots of the figure
plt.subplots_adjust(left=0.15)

axcolor = 'lightgoldenrodyellow'
rax = plt.axes([0, 0.8, 0.1, 0.1], facecolor=axcolor)
radio = RadioButtons(rax, ('On', 'Off'))

def toggleLabel(label):
    toggle = None
    if label == 'On':
        toggle = True
    else :
        toggle = False
    for label in text_labels:
        label.set_visible(toggle)
    plt.draw()

radio.on_clicked(toggleLabel)
# print(model.most_similar(positive=['lovelymrsyi']))
#
# for value in points.values:
#     if value[0] =='lovelymrsyi':
#         print(value)


plt.show()