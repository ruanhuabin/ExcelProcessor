# encoding: utf-8
'''
Created on 2016��9��14��

@author: ruanhuabin
'''
from Tkinter import *
from tkFileDialog import askopenfilename
from tkFileDialog import askdirectory
from _functools import partial
#from Screen import init

from Screen import init, printDict, checkFileValid, extractCompoundNameColumn,\
    extractMZExpectColumn, genRTColumn, genLibraryScoreColumn, genIPColumn,\
    genLSColumn, genRTRangeColumn, genMZDeltaColumn, genMeasuredAreaColumn,\
    genRTMeasuredColumn
from constant import *
from util import extractMZExpectData, writeWordBook
import tkMessageBox


class Application:
    def __init__(self, master):
        frame = Frame(master,width=400,height=600)
        frame.pack()   
        
        self.inputFilePath =StringVar()
        self.labelFolder = Label(frame,textvariable=self.inputFilePath).grid(row=0,columnspan=2)
        
        self.log_file_btn = Button(frame, text="Select Screen File", command=self.selectInputFile).grid(row=1, columnspan=2)
        
        self.outputFolderPath = StringVar()
        self.labelImageFile = Label(frame,textvariable = self.outputFolderPath).grid(row = 2, columnspan = 2)
        self.output_folder_btn = Button(frame, text="Output Folder", command=self.selectOutputFolder,width=40).grid(row=3, columnspan=2)
        
        self.blankText = StringVar()
        self.blankLabel = Label(frame,textvariable = self.blankText).grid(row = 4, columnspan = 2)
        
        self.output_filename_label = Label(frame, text="Output File Name:          ")#.grid(row=5, columnspan=2)
        self.output_filename_label.grid(row=5, columnspan=2)
       
        self.output_filename_entry = Entry(frame, width=30, bd = 4)
        self.output_filename_entry.grid(row=6, column=0, columnspan=2)
        
        
        f = frame
        xscrollbar = Scrollbar(f, orient=HORIZONTAL)
        xscrollbar.grid(row=12, column=0, sticky=N+S+E+W)
 
        yscrollbar = Scrollbar(f)
        yscrollbar.grid(row=11, column=1, sticky=N+S+E+W)
 
        self.text_field = Text(f, wrap=NONE,
                    xscrollcommand=xscrollbar.set,
                    yscrollcommand=yscrollbar.set)
        self.text_field.grid(row=11, column=0)
 
        xscrollbar.config(command=self.text_field.xview)
        yscrollbar.config(command=self.text_field.yview)
      

        
        
        self.blankText = StringVar()
        self.blankLabel = Label(frame,textvariable = self.blankText).grid(row = 7, columnspan = 2)
        
        self.start_run_btn = Button(frame, text="Start Processing", command=partial(self.startProcessing, self.text_field), width=40).grid(row=8, columnspan=2)
        
        self.blankText = StringVar()
        self.blankLabel = Label(frame,textvariable = self.blankText).grid(row = 9, columnspan = 2)
        self.counter = 0
        
        self.inputDataBook = {}
        self.outputDataBook = {}
        self.inputFilename = ""
        

  

    def selectInputFile(self):
        filename = askopenfilename()
        self.inputFilePath.set(filename)
        self.inputFilename = filename
        
      
        
       

    def selectOutputFolder(self):
        imageFolder = askdirectory()
        self.outputFolderPath.set(imageFolder)
    
    def startProcessing(self, text_field):
        if(self.inputFilePath.get() == ""):
            tkMessageBox.showerror("Error", "Please select a screen file to be processed")
            return
        if(self.outputFolderPath.get() == ""):
            self.outputFolderPath.set("./")
#             tkMessageBox.showerror("Error", "Please select a output folder to save the file: %s" % self.outputFolderPath.get())
#             return
        if(self.output_filename_entry.get() == ""):
           # print "text-field = ", self.text_field.get()
            tkMessageBox.showerror("Error", "Please enter a filename for the output file" )
            return
        
        outputFolderPath = self.outputFolderPath.get()
        if(outputFolderPath[-1] != '/'):
            outputFolderPath = outputFolderPath + "/"
            
        outputFilename = outputFolderPath + self.output_filename_entry.get()
        
        filenameExtension = outputFilename.split(".")[-1]
        if(filenameExtension != "xlsx"):
            outputFilename = outputFilename + ".xlsx"
        
        
               
        text_field.insert(INSERT, "%d: Start to Process file: %s\n" % (self.counter, self.inputFilePath.get()))        
        self.counter = self.counter + 1
       
        
        rowTitleMust = [compoundNameTitle, mzExpectedTitle, libraryScoreTitle, measuredAreaTitle, ipTitle, lsTitle, rtMeasuredTitle, mzDeltaTitle]
        text_field.insert(INSERT, "%d: Start Loading Data: %s\n" %(self.counter, self.inputFilePath.get()))
        self.counter += 1
        [self.inputDataBook, self.outputDataBook] = init(self.inputFilename)
        text_field.insert(INSERT, "%d: Finish Loading Data: %s\n" %(self.counter, self.inputFilePath.get()))
        self.counter += 1
        
        print "self.inputDataBook = ", self.inputDataBook
        #printDict(self.inputDataBook)
        [missingNum, missingRowTitleDict] = checkFileValid(self.inputDataBook,  rowTitleMust )
        text_field.insert(INSERT, "%d: Check file validation complete\n" %(self.counter))
        self.counter += 1
        if(missingNum > 0):
            print "Error: Some worksheet missing some column(s):"
            printDict(missingRowTitleDict)
            text_field.insert(INSERT, "%d: Missing Columns: %s\n" %(self.counter, str(missingRowTitleDict)))
            self.counter += 1    
            text_field.insert(INSERT, "%d: Error: Some worksheet missing some column(s), see missing column above\n" %(self.counter))
            self.counter += 1
            raise ValueError("Error: Some worksheet missing some column(s), see missing column above")
        compoundNames = extractCompoundNameColumn(self.inputDataBook, self.outputDataBook)
        text_field.insert(INSERT, "%d: Extract compound names success: compound Names are: %s\n" %(self.counter, str(compoundNames)))
        self.counter += 1
        extractMZExpectColumn(self.inputDataBook, compoundNames, self.outputDataBook)
        text_field.insert(INSERT, "%d: Extract m/z expected data success\n" %(self.counter))
        self.counter += 1
        genRTColumn(self.inputDataBook, compoundNames, self.outputDataBook)
        text_field.insert(INSERT, "%d: Extract RT Value success\n" %(self.counter))
        self.counter += 1
        genLibraryScoreColumn(self.inputDataBook, compoundNames, self.outputDataBook)
        text_field.insert(INSERT, "%d: Extract library score success\n" %(self.counter))
        self.counter += 1
        genIPColumn(self.inputDataBook, compoundNames, self.outputDataBook)
        text_field.insert(INSERT, "%d: Extract  IP success\n" %(self.counter))
        self.counter += 1
        genLSColumn(self.inputDataBook, compoundNames, self.outputDataBook)
        text_field.insert(INSERT, "%d: Extract LS data success\n" %(self.counter))
        self.counter += 1
        genRTRangeColumn(self.inputDataBook, compoundNames, self.outputDataBook)
        text_field.insert(INSERT, "%d: Extract RT Range success\n" %(self.counter))
        self.counter += 1
        genMZDeltaColumn(self.inputDataBook, compoundNames, self.outputDataBook)
        text_field.insert(INSERT, "%d: Extract M/Z Delta success\n" %(self.counter))
        self.counter += 1
        genMeasuredAreaColumn(self.inputDataBook, compoundNames, self.outputDataBook)
        text_field.insert(INSERT, "%d: Extract Measure Area success\n" %(self.counter))
        self.counter += 1
        genRTMeasuredColumn(self.inputDataBook, compoundNames, self.outputDataBook)
        text_field.insert(INSERT, "%d: Extract RT Measure success\n" %(self.counter))
        self.counter += 1
        writeWordBook(self.outputDataBook, outputFilename)
        text_field.insert(INSERT, "%d: Job Complete Successfully, Output File Name: %s!!! \n" %(self.counter, outputFilename))
        self.counter += 1
        
        
        
        
        text_field.see("end")
        
        
        
        

mainFrame = Tk()
mainFrame.title("Screen Data Processor")
mainFrame.geometry("600x800")
mainFrame.resizable(False, False)
app = Application(mainFrame)
mainFrame.mainloop()