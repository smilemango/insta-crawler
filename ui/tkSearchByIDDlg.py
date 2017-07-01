import my_logger
import ui.tkSimpleDialog as tsdlg
import tkinter as Tk

#검색한 ID가 팔로잉한 ID를 화면에 표시해주는 기능
#ID를 검색하기 위해 다이얼로그를 띄워줌
class SearchByIDDlg(tsdlg.Dialog):

    def __init__(self,parent,db_conn,callback):
        self.conn = db_conn
        self.callback = callback
        self.logger = my_logger.init_mylogger("follows2vec_logger","./log/follows2vec.log")
        tsdlg.Dialog.__init__(self,parent=parent, modal = False,title="[SCHBI] 아이디 검색")

    def doSearch(self):
        self.logger.info("Do Search Action")

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
