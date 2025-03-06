#! /usr/bin/env python3
#  -*- coding: utf-8 -*-
#
# GUI module generated by PAGE version 8.0
#  in conjunction with Tcl version 8.6
#    Mar 06, 2025 03:01:02 PM CST  platform: Windows NT

import sys
import tkinter as tk
import tkinter.ttk as ttk
from tkinter.constants import *
import os.path

_location = os.path.dirname(__file__)

import nobuonGui_support

_bgcolor = '#d9d9d9'
_fgcolor = '#000000'
_tabfg1 = 'black' 
_tabfg2 = 'white' 
_bgmode = 'light' 
_tabbg1 = '#d9d9d9' 
_tabbg2 = 'gray40' 

class Toplevel1:
    def __init__(self, top=None):
        '''This class configures and populates the toplevel window.
           top is the toplevel containing window.'''

        top.geometry("289x338+709+491")
        top.minsize(120, 1)
        top.maxsize(5124, 1061)
        top.resizable(1,  1)
        top.title("信on小工具")
        top.configure(background="#d9d9d9")
        top.configure(highlightbackground="#d9d9d9")
        top.configure(highlightcolor="#000000")

        self.top = top
        self.winList = tk.StringVar()

        self.Func_Listbox = tk.Listbox(self.top)
        self.Func_Listbox.place(relx=0.519, rely=0.118, relheight=0.592
                , relwidth=0.436)
        self.Func_Listbox.configure(background="white")
        self.Func_Listbox.configure(disabledforeground="#a3a3a3")
        self.Func_Listbox.configure(font="TkFixedFont")
        self.Func_Listbox.configure(foreground="#000000")
        self.Func_Listbox.configure(highlightbackground="#d9d9d9")
        self.Func_Listbox.configure(highlightcolor="#000000")
        self.Func_Listbox.configure(selectbackground="#d9d9d9")
        self.Func_Listbox.configure(selectforeground="black")

        self.Win_Listbox = tk.Listbox(self.top)
        self.Win_Listbox.place(relx=0.035, rely=0.118, relheight=0.592
                , relwidth=0.415)
        self.Win_Listbox.configure(background="white")
        self.Win_Listbox.configure(disabledforeground="#a3a3a3")
        self.Win_Listbox.configure(font="TkFixedFont")
        self.Win_Listbox.configure(foreground="#000000")
        self.Win_Listbox.configure(highlightbackground="#d9d9d9")
        self.Win_Listbox.configure(highlightcolor="#000000")
        self.Win_Listbox.configure(selectbackground="#d9d9d9")
        self.Win_Listbox.configure(selectforeground="black")
        self.Win_Listbox.configure(listvariable=self.winList)

        self.goButton = tk.Button(self.top)
        self.goButton.place(relx=0.035, rely=0.769, height=36, width=68)
        self.goButton.configure(activebackground="#d9d9d9")
        self.goButton.configure(activeforeground="black")
        self.goButton.configure(background="#d9d9d9")
        self.goButton.configure(disabledforeground="#a3a3a3")
        self.goButton.configure(foreground="#000000")
        self.goButton.configure(highlightbackground="#d9d9d9")
        self.goButton.configure(highlightcolor="#000000")
        self.goButton.configure(text='''Go''')

        self.msgMessage = tk.Message(self.top)
        self.msgMessage.place(relx=0.311, rely=0.769, relheight=0.175
                , relwidth=0.64)
        self.msgMessage.configure(background="#d9d9d9")
        self.msgMessage.configure(foreground="#000000")
        self.msgMessage.configure(highlightbackground="#d9d9d9")
        self.msgMessage.configure(highlightcolor="#000000")
        self.msgMessage.configure(padx="1")
        self.msgMessage.configure(pady="1")
        self.msgMessage.configure(text='''中文測試''')
        self.msgMessage.configure(width=185)

def start_up():
    nobuonGui_support.main()

if __name__ == '__main__':
    nobuonGui_support.main()




