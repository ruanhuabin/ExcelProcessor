# encoding: utf-8
'''
Created on 2016��9��14��

@author: ruanhuabin
'''
from Tkinter import *
from tkFileDialog import askopenfilename
from tkFileDialog import askdirectory
from _functools import partial


class Application:
    def __init__(self, master):
        frame = Frame(master,width=400,height=600)
        frame.pack()

        
        self.inputFilePath =StringVar()
        self.labelFolder = Label(frame,textvariable=self.inputFilePath).grid(row=0,columnspan=2)
        
        self.log_file_btn = Button(frame, text="Select Screen File", command=self.selectInputFile,width=40, height=1).grid(row=1, columnspan=2)
        
        
        self.outputFolderPath = StringVar()
        self.labelImageFile = Label(frame,textvariable = self.outputFolderPath).grid(row = 2, columnspan = 2)
        self.output_folder_btn = Button(frame, text="Output Folder", command=self.selectOutputFolder,width=40).grid(row=3, columnspan=2)
        
        self.blankText = StringVar()
        self.blankLabel = Label(frame,textvariable = self.blankText).grid(row = 4, columnspan = 2)

        
        self.output_filename_label = Label(frame, text="\t\t\tOutput File Name: ")#.grid(row=5, columnspan=2)
        self.output_filename_label.grid(row=5, columnspan=1)
       
        self.output_filename_entry = Entry(frame, width = 30, bd = 4).grid(row=6, column=0, columnspan=1)
        
        self.blankText = StringVar()
        self.blankLabel = Label(frame,textvariable = self.blankText).grid(row = 6, columnspan = 2)
        
        
        xscrollbar = Scrollbar(frame, orient=HORIZONTAL)
        xscrollbar.grid(row=10, column=0, columnspan = 2, sticky=N+S+E+W)

        yscrollbar = Scrollbar(frame, orient=VERTICAL)
        yscrollbar.grid(row=9, column=1, sticky=N+S+E+W)
        
        
        self.text_field = Text(frame, wrap=NONE, height=10, xscrollcommand=xscrollbar.set, yscrollcommand=yscrollbar.set)#.grid(row = 9, columnspan=2)
        self.text_field.grid(row = 9, column = 0, columnspan=2)
        
        xscrollbar.config(command=self.text_field.xview)
        yscrollbar.config(command=self.text_field.yview)
        
        self.start_run_btn = Button(frame, text="Start Processing", command=partial(self.startProcessing, self.text_field), width=40).grid(row=7, columnspan=2)
        
#         self.blankText = StringVar()
#         self.blankLabel = Label(frame,textvariable = self.blankText).grid(row = 8, columnspan = 2)  

    def selectInputFile(self):
        filename = askopenfilename()
        self.inputFilePath.set(filename)

    def selectOutputFolder(self):
        imageFolder = askdirectory()
        self.outputFolderPath.set(imageFolder)
    
    def startProcessing(self, text_field):#       
        text_field.insert(INSERT, "Start to Process file: %s\n" % self.inputFilePath.get())
        text_field.see("end")
        

mainFrame = Tk()
mainFrame.title("Screen Data Processor")
mainFrame.geometry("600x800")
#mainFrame.resizable(False, False)
app = Application(mainFrame)
mainFrame.mainloop()