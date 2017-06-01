import matplotlib
matplotlib.use('TkAgg')

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


# SAVED_FILE_PATH = "./vector/follows2vec_500_20_0.w2v"
# model = gensim.models.Word2Vec.load(SAVED_FILE_PATH)
# #my video - how to visualize a dataset easily
# tsne = sklearn.manifold.TSNE(n_components=2, random_state=0)
# all_word_vectors_matrix = model.wv.syn0
# #pp.pprint(model.wv.syn0[0])
#
# all_word_vectors_matrix_2d = tsne.fit_transform(all_word_vectors_matrix)
#
# points = pd.DataFrame(
#     [
#         (word, coords[0], coords[1])
#         for word, coords in [
#             (word, all_word_vectors_matrix_2d[model.wv.vocab[word].index])
#             for word in model.wv.vocab
#         ]
#     ],
#     columns=["word", "x", "y"]
# )

"""
---------------------------------
"""
root = Tk.Tk()
root.wm_title("Embedding in TK")


f = Figure(figsize=(5, 4), dpi=100)
ax = f.add_subplot(111)

#a.plot(t, s)
#ax.scatter(points['x'], points['y'], alpha=0.7, s=[5] * len(points['x']))

points = pd.DataFrame(
    [('word0',0,0),('word1',1,1),('word2',2,2)],
    columns=["word","x","y"]
)

ax.scatter(points['x'], points['y'], alpha=0.7, s=[5] * len(points['x']))
text_labels = []
for i, point in points.iterrows():
    t= ax.text(point.x + 0.0001, point.y, point.word, fontsize=10, alpha=0.8, url="http://www.instagram.com/" + point.word)
    text_labels.append( t)




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
    if btnToggle.config('text')[-1] == 'True':
        btnToggle.config(text='False')
    else:
        btnToggle.config(text='True')

    if btnToggle.config('text')[-1] == 'True':
        for label in text_labels:
            label.set_visible(True)
    else:
        for label in text_labels:
            label.set_visible(False)
    canvas.draw()


bottom_panel = Tk.PanedWindow(master=root)
bottom_panel.pack(side=Tk.BOTTOM)

txtSearch = Tk.Text(master=bottom_panel,height=1,width=10)
txtSearch.pack(side=Tk.LEFT)

btnSearch = Tk.Button(master=bottom_panel, text="검색")
btnSearch.pack(side=Tk.LEFT)

btnToggle = Tk.Button(master=bottom_panel, text="True", width=12, command=toggle)
btnToggle.pack(side=Tk.LEFT)

btnQuit = Tk.Button(master=bottom_panel, text='Quit', command=_quit)
btnQuit.pack(side=Tk.LEFT)

Tk.mainloop()
# If you put root.destroy() here, it will cause an error if
# the window is closed with the window manager.