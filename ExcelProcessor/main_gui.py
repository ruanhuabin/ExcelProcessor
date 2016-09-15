# encoding: utf-8
'''
Created on 2016��9��14��

@author: ruanhuabin
'''

import Tkinter
from Tkinter import Button, Label
from Tkconstants import *
from tkFileDialog import askopenfilename
from Tkinter import Tk
from _functools import partial

def hello(win, filenameLabel):
    print "Hello world"
    filename = askopenfilename()
    filenameLabel.config(text=filename, width="100")
    print filename

win = Tkinter.Tk()
win.title("Screen Data Processor")
win.geometry('400x200')

filenameLabel = Label(win, text="Hello Eric")
filenameLabel.pack(side=TOP)

btn = Button(win, text="StartProcess", command = partial(hello, win, filenameLabel))
btn.pack(side=TOP)



win.mainloop()
if __name__ == '__main__':
    pass