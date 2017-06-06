import my_logger
import ui.tkSimpleDialog as tsdlg
import tkinter as Tk

class SimilarByIDDlg(tsdlg.Dialog):

    def __init__(self,parent,callback):
        self.logger = my_logger.init_mylogger("follows2vec_logger","./log/follows2vec.log")
        self.callback = callback
        tsdlg.Dialog.__init__(self,parent=parent, modal = False,title="유사아이디 검색")

    def doSearch(self):
        self.logger.info("Do Search Action")
        result = self.callback(self.etSearch.get())

        self.logger.info(result)
        self.txtResult.delete(0, Tk.END)
        self.txtResult.insert(Tk.END, result)


    def body(self, master):

        f = Tk.Frame(self)

        self.etSearch = Tk.Entry(f)
        self.btnSearch = Tk.Button(f,text="찾기",command=self.doSearch)
        self.txtResult = Tk.Text(master)
        self.scrollbar = Tk.Scrollbar(master)

        self.etSearch.pack(side= Tk.LEFT)
        self.btnSearch.pack(side=Tk.RIGHT)

        f.pack(side=Tk.TOP)
        self.scrollbar.pack(side=Tk.RIGHT, fill=Tk.Y)
        self.txtResult.pack()
        # attach listbox to scrollbar
        self.txtResult.config(yscrollcommand=self.scrollbar.set)
        self.scrollbar.config(command=self.txtResult.yview)

        return self.etSearch # initial focus

    def apply(self):
        pass
