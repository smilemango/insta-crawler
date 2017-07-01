import my_logger
import ui.tkSimpleDialog as tsdlg
import tkinter as Tk

class SearchSimilarByIDDlg(tsdlg.Dialog):
    def __init__(self, parent,model,callback):
        self.model = model
        self.callback = callback
        tsdlg.Dialog.__init__(self,parent=parent, title="[SMBI] 아이디 목록 검색")

    def body(self,master):
        top_f = Tk.Frame(self)

        self.etSearch = Tk.Entry(top_f)
        self.btnSearch = Tk.Button(top_f,text="찾기", command=self.searchIds)


        self.etSearch.pack(side=Tk.LEFT)
        self.btnSearch.pack(side=Tk.RIGHT)

        self.btnOk = Tk.Button(master,text="Apply", command=self.ok)

        top_f.pack(side=Tk.TOP)

        self.scrollbar = Tk.Scrollbar(master)
        self.scrollbar.pack(side=Tk.RIGHT, fill=Tk.Y)

        self.lstResult = Tk.Listbox(master)
        self.lstResult.pack(fill=Tk.BOTH )

        self.btnOk.pack(side=Tk.BOTTOM)

        # attach listbox to scrollbar
        self.lstResult.config(yscrollcommand=self.scrollbar.set)
        self.scrollbar.config(command=self.lstResult.yview)

        return self.etSearch  # initial focus

    def searchIds(self):

        self.lstResult.delete(0, Tk.END)

        q_word = self.etSearch.get()

        keys = list(self.model.wv.vocab.keys())
        for key in keys:
            if q_word in key :
                self.lstResult.insert(Tk.END, "%s (%d)" % ( key, self.model.wv.vocab[key].count))

    def ok(self):

        seleted_word = self.lstResult.get(Tk.ACTIVE).split(' ')[0]
        self.callback(seleted_word)
        super(SearchSimilarByIDDlg,self).ok()

class SimilarByIDDlg(tsdlg.Dialog):

    def __init__(self,parent,model, callback):
        self.logger = my_logger.init_mylogger("follows2vec_logger","./log/follows2vec.log")
        self.model = model
        self.callback = callback
        tsdlg.Dialog.__init__(self,parent=parent, modal = False,title="유사아이디 검색")

    def openSimilarDlg(self):
        SearchSimilarByIDDlg(self,self.model,callback=self.setID)


    def setID(self, id):
        self.etSearch.delete(0, Tk.END)
        self.etSearch.insert(0, id)

    def doGo(self):
        id = self.etSearch.get()

        lstResult = self.model.most_similar(positive=id, topn=10)
        self.lstResult.delete(0, Tk.END)
        for row in lstResult :
            self.lstResult.insert(Tk.END, "%s (%f)" % (row[0], row[1]) )

    def doDoubleClick(self,event):
        ##this block works
        w = event.widget
        tpl_users = w.get(0,w.size())

        lst_ret_users = []
        lst_ret_users.append(self.etSearch.get())

        for item in tpl_users:
            lst_ret_users.append( item.split()[0])

        self.callback(lst_ret_users)


    def body(self, master):

        f = Tk.Frame(self)

        self.etSearch = Tk.Entry(f)
        self.btnSearch = Tk.Button(f, text="아이디 설정...", command=self.openSimilarDlg)
        self.btnGo = Tk.Button(f,text="GO!",command=self.doGo)
        self.lstResult = Tk.Listbox(master)
        self.lstResult.bind("<Double-Button-1>", self.doDoubleClick)
        self.scrollbar = Tk.Scrollbar(master)

        self.etSearch.pack(side= Tk.LEFT)
        self.btnSearch.pack(side=Tk.RIGHT)
        self.btnGo.pack(side=Tk.RIGHT)

        f.pack(side=Tk.TOP)
        self.scrollbar.pack(side=Tk.RIGHT, fill=Tk.Y)
        self.lstResult.pack()
        # attach listbox to scrollbar
        self.lstResult.config(yscrollcommand=self.scrollbar.set)
        self.scrollbar.config(command=self.lstResult.yview)

        return self.etSearch # initial focus

    def apply(self):
        pass
