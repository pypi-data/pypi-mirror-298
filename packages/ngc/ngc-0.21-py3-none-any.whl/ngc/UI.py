#!/usr/bin/env python3
# -*- coding:utf-8 -*-
import sys
from tkinter import *
from tkinter.ttk import *



class UIStack:
    def __init__(self, mylist):
        self.dblist = []
        self.StringStacks = {}
        global dblist
        root = Tk()
        if 'title' in mylist:
            root.title(mylist['title'])
        else:
            root.title(sys.argv[0])
        flist = mylist['function']
        i = 1
        for item in flist:
            y = 1
            func = flist[item]
            db = StringVar()
            self.dblist.append(db)
            # db = StringVar()
            inputme = Entry(root, width=80, textvariable=db)
            inputme['state'] = 'write'
            inputme.grid(row=i, column=1, padx=3, pady=3, sticky=W + E)
            self.StringStacks[item] = db
            if func!= None:
                pushme = Button(root, text=item, command=func)
            else:
                pushme = Button(root, text=item)
            pushme.grid(row=i, column=2, sticky=W, padx=(2, 0), pady=(2, 0))

            i += 1
        root.columnconfigure(2, weight=1)
        root.mainloop()

if __name__ == '__main__':
    def func1():
        print('001')
    # def func2():
    #     for it in StringStacks:
    #         print(StringStacks[it].get())
    mylist = {
        "function": {
            "text1": func1,
            # "text2": func2
        }
    }
    myui = UIStack(mylist)
