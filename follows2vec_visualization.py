import matplotlib
matplotlib.use('TkAgg')

import sqlite3
import logging
import pprint as pp
import matplotlib.pyplot as plt
import os, sys
import multiprocessing
from matplotlib import font_manager, rc
import my_logger
import ui.tkSimpleDialog as tsdlg

from numpy import arange, sin, pi
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2TkAgg
# implement the default mpl key bindings
from matplotlib.backend_bases import key_press_handler
from matplotlib.figure import Figure
import tkinter as Tk
import gensim
import sklearn
from sklearn.manifold import TSNE
import pandas as pd

logger = my_logger.init_mylogger("follows2vec_logger","./log/follows2vec.log")

# 클러스터링 관련 : https://github.com/gaetangate/word2vec-cluster 의 소스를 참고할 것

class SearchByIDDlg(tsdlg.Dialog):

    def __init__(self,parent,db_conn,callback):
        self.conn = db_conn
        self.callback = callback
        tsdlg.Dialog.__init__(self,parent=parent, modal = False,title="아이디 검색")

    def doSearch(self):
        logger.info("Do Search Action")

        c = self.conn.cursor()
        c.execute("""
SELECT username, count(*) as CNT
FROM users, relations
WHERE users.id = relations.user_id
AND users.username like '%s%%'
GROUP BY username
ORDER BY CNT;
""" % self.etSearch.get())
        rs = c.fetchall()
        print(rs)

        self.lstResult.delete(0, Tk.END)
        for row in rs :
            self.lstResult.insert(Tk.END, "%s (%d)" % (row[0], row[1]) )


    def doDoubleClick(self,event):
        ##this block works
        w = event.widget
        index = int(w.curselection()[0])
        value = w.get(index)
        print(value)
        username = value.split()[0]
        self.callback(username)


    def body(self, master):


        f = Tk.Frame(self)

        self.etSearch = Tk.Entry(f)
        self.btnSearch = Tk.Button(f,text="찾기",command=self.doSearch)
        self.lstResult = Tk.Listbox(master)
        self.lstResult.bind("<Double-Button-1>", self.doDoubleClick)

        self.scrollbar = Tk.Scrollbar(master)

        self.etSearch.pack(side= Tk.LEFT)
        self.btnSearch.pack(side=Tk.RIGHT)

        f.pack(side=Tk.TOP)
        self.scrollbar.pack(side=Tk.RIGHT, fill=Tk.Y)
        self.lstResult.pack()
        # attach listbox to scrollbar
        self.lstResult.config(yscrollcommand=self.scrollbar.set)
        self.scrollbar.config(command=self.lstResult.yview)

        return self.etSearch # initial focus

    def apply(self):
        pass



if __name__ == '__main__':

    conn = sqlite3.connect('processed_data/insta_user_relations.sqlite3')

    do_word2vec = True

    if do_word2vec :
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
        min_word_count = 150

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
        model = None

        if not os.path.isfile(SAVED_FILE_PATH):
            logger.info("Vector data does not exist.")
            conn = sqlite3.connect('processed_data/insta_user_relations.sqlite3')
            c = conn.cursor()

            logger.info("Loading Database.")
            points_by_cluster = pd.read_sql_query("""
            SELECT
                (SELECT username FROM users WHERE id = A.user_id) user_id,
                (SELECT username FROM users WHERE id = A.follow_id) follow_id
            FROM relations A
            --limit 100 ;
            """, conn)
            logger.info("Database loading completed.")
            logger.info("Data transforming... Group By 'USER_ID'")
            trans =  points_by_cluster.groupby('user_id')['follow_id'].apply(lambda x: ",".join(x.astype(str)))
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


        logger.info("Vector data already exists.")
        logger.info("Load data...")
        model = gensim.models.Word2Vec.load(SAVED_FILE_PATH)

        """
        ---------------------------------
        """
        tsne = sklearn.manifold.TSNE(n_components=2, random_state=0)
        all_word_vectors_matrix = model.wv.syn0
        pp.pprint(model.wv.syn0[0])

        logger.info("Vector to 2d matrix.")
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

    else :
        logger.info("Initialize data for testing.")
        points = pd.DataFrame([['a',100,100],['b',-100,-100],['c',100,-100]],columns=['word','x','y'])

    logger.info("Intialize UI")
    root = Tk.Tk()
    root.wm_title("Embedding in TK")


    f = Figure(figsize=(5, 4), dpi=100)
    ax = f.add_subplot(111)
    #username으로 검색해서 화면에 찍은 점
    global sct_by_username
    #my video - how to visualize a dataset easily


    if sys.platform == 'win32':
        font_name = font_manager.FontProperties(fname="c:/Windows/Fonts/malgun.ttf").get_name()
        rc('font', family=font_name)
    elif sys.platform == 'darwin':
        rc('font', family="AppleGothic")

    plt.rcParams['axes.unicode_minus'] = False

    from sklearn.cluster import KMeans
    import numpy as np

    logger.info("Clustring...")
    kmeans = KMeans(n_clusters=10 if len(points) >= 10 else len(points), n_jobs=-1, random_state=0)
    #cluster_idx = kmeans.fit_predict(points[["x","y"]])
    kmeans.fit(points[["x","y"]])
    cluster_idx = kmeans.labels_
    logger.info("Clustering...DONE")

    points['cluster']= pd.Series(np.asarray(cluster_idx))

    cluster = {}
    for idx, point in points.iterrows():
        if point['cluster'] in cluster :
            cluster[point['cluster']].append(idx)
        else :
            cluster[point['cluster']] = []
            cluster[point['cluster']].append(idx)


    #점을 표시해준다.
    for c in cluster:
        points_by_cluster = pd.DataFrame(columns=('x', 'y', 'word', 'cluster'))
        for idx in cluster[c]:
            points_by_cluster = points_by_cluster.append(points.iloc[[idx]])
        #list = [points.iloc[[idx]] for idx in cluster[c]]
        ax.scatter(points_by_cluster['x'], points_by_cluster['y'], alpha=0.7 )

    text_labels = []
    for i, point in points.iterrows():
        #텍스트 라벨을 표시해준다
        t= ax.text(point.x + 0.0001, point.y, point.word, fontsize=10, alpha=0.8, url="http://www.instagram.com/" + point.word)
        t.set_visible(False)
        text_labels.append(t)


    # a tk.DrawingArea
    canvas = FigureCanvasTkAgg(f, master=root)
    canvas.show()
    canvas.get_tk_widget().pack(side=Tk.TOP, fill=Tk.BOTH, expand=1)

    toolbar = NavigationToolbar2TkAgg(canvas, root)
    toolbar.update()
    canvas._tkcanvas.pack(side=Tk.TOP, fill=Tk.BOTH, expand=1)


    def on_key_event(event):
        print('you pressed %s' % event.key)
        key_press_handler(event, canvas, toolbar)

    canvas.mpl_connect('key_press_event', on_key_event)


    def _quit():
        root.quit()     # stops mainloop
        root.destroy()  # this is necessary on Windows to prevent
                        # Fatal Python Error: PyEval_RestoreThread: NULL tstate


    def toggle():
        if btnToggle.config('text')[-1] == '라벨 감추기':
            btnToggle.config(text='라벨 보여주기')
        else:
            btnToggle.config(text='라벨 감추기')

        if btnToggle.config('text')[-1] == '라벨 감추기':
            for label in text_labels:
                label.set_visible(True)
        else:
            for label in text_labels:
                label.set_visible(False)
        canvas.draw()

    def openSearchDialog():
        logger.info("Open SearchDailog")

        d= SearchByIDDlg(parent=root,db_conn=conn,callback=setUsername)
        logger.info(d.result)

    def setUsername(username):
        global sct_by_username
        logger.info("Set Username")

        #1. SELECT FOLLOWS BY username
        #2. SCATTER POINTS
        #3. SET LABEL BY username
        etUsername.config(state=Tk.NORMAL)
        etUsername.delete(0, Tk.END)
        etUsername.insert(0, username)
        etUsername.config(state=Tk.DISABLED)

        c = conn.cursor()
        c.execute(
"""
SELECT (SELECT username FROM users WHERE id = relations.follow_id) as ids
FROM relations
WHERE user_id = (SELECT id FROM users WHERE username='%s')
""" % ( username ))

        rs = c.fetchall()
        logger.info(rs)

        points_by_user = pd.DataFrame()
        for row in rs :
            points_by_user = points_by_user.append( points[points['word'] == row[0]])

        sct_by_username =  ax.scatter(points_by_user["x"],points_by_user["y"],c='r', marker="^")

        canvas.draw()


    def clearUsername():
        global sct_by_username

        logger.debug("Clear Username")
        etUsername.config(state=Tk.NORMAL)
        etUsername.delete(0, Tk.END)
        etUsername.config(state=Tk.DISABLED)

        if sct_by_username != None:
            sct_by_username.remove()

        canvas.draw()

    bottom_panel = Tk.PanedWindow(master=root)
    bottom_panel.pack(side=Tk.BOTTOM)

    lbShow = Tk.Label(master=bottom_panel, text="표시")
    lbShow.pack(side=Tk.LEFT)

    etUsername = Tk.Entry(master=bottom_panel)
    etUsername.config(state=Tk.DISABLED)
    etUsername.pack(side=Tk.LEFT)

    btnSet = Tk.Button(master=bottom_panel, text="설정...", command=openSearchDialog)
    btnSet.pack(side=Tk.LEFT)

    btnClear =Tk.Button(master=bottom_panel, text="지우기", command=clearUsername)
    btnClear.pack(side=Tk.LEFT)


    lbSep = Tk.Label(master=bottom_panel, text="    ")
    lbSep.pack(side=Tk.LEFT)

    btnToggle = Tk.Button(master=bottom_panel, text="라벨 감추기", width=12, command=toggle)
    btnToggle.pack(side=Tk.LEFT)

    btnQuit = Tk.Button(master=bottom_panel, text='Quit', command=_quit)
    btnQuit.pack(side=Tk.LEFT)

    Tk.mainloop()
    # If you put root.destroy() here, it will cause an error if
    # the window is closed with the window manager.