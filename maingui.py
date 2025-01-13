import tkinter

def gofunc():
    print("This is go func!!")
    listbox_window.insert(tkinter.END,"視窗4")
    statustext.set("gofunc click!!")

top=tkinter.Tk()
top.title("信長小工具")
width = 400
height = 300
left = (top.winfo_screenwidth() - width)*2 / 3
right = (top.winfo_screenheight() - height)*2 / 3
top.geometry("%dx%d+%d+%d" % (width, height, left, right))
#top.geometry("400x300")

lbltext1 = tkinter.Label(top,text="視窗列表")
lbltext2 = tkinter.Label(top,text="功能列表")
listbox_window = tkinter.Listbox(top)
listbox_window.insert(tkinter.END,"視窗1")
listbox_window.insert(tkinter.END,"視窗2")
listbox_window.insert(tkinter.END,"視窗3")

listbox_func = tkinter.Listbox(top)
listbox_func.insert(tkinter.END,"功能1")
listbox_func.insert(tkinter.END,"功能2")
listbox_func.insert(tkinter.END,"功能3")

btngo = tkinter.Button(top,text="GO",command=gofunc)

statustext = tkinter.StringVar()
statuslabel = tkinter.Label(top,textvariable=statustext,font=("Arial",10))
statustext.set("Ready")

lbltext1.grid(row=0,column=0)
lbltext2.grid(row=0,column=1)
listbox_window.grid(row=1,column=0)
listbox_func.grid(row=1,column=1)
statuslabel.grid(row=3,column=0, rowspan=2, sticky=tkinter.W)
btngo.grid(row=2,column=0)
top.mainloop()