from tkinter import *
from  tkinter import ttk


ws  = Tk()
ws.title('PythonGuides')
ws.geometry('300x400')

set = ttk.Treeview(ws)
set.pack()

set['columns']= ('id', 'full_Name','award')
set.column("#0", width=0,  stretch=NO)
set.column("id",anchor=CENTER, width=80)
set.column("full_Name",anchor=CENTER, width=80)
set.column("award",anchor=CENTER, width=80)

set.heading("#0",text="",anchor=CENTER)
set.heading("id",text="ID",anchor=CENTER)
set.heading("full_Name",text="Full_Name",anchor=CENTER)
set.heading("award",text="Award",anchor=CENTER)

set.insert(parent='',index='end',iid=0,text='',
values=('101','john','Gold'))
set.insert(parent='',index='end',iid=1,text='',
values=('102','jack',"Silver"))
set.insert(parent='',index='end',iid=2,text='',
values=('103','joy','Bronze'))

ws.mainloop()