#!/usr/bin/env python
# encoding: utf-8
#from util import writeWordBook, initNewWordBook, writeDataToColumn, extractMZExpectData,\
#    loadData

from util import writeWordBook, initNewWordBook, writeDataToColumn, extractMZExpectData, loadData
from subprocess import Popen
from popen2 import popen4
from os import system
from time import time, sleep
import sys


newScreenBook = initNewWordBook()
screenDataBook = loadData("small-screen.xlsx")
sheetNames = list(screenDataBook)
sheetNames.sort()
print sheetNames
print len(sheetNames)

compoundNameTitle = "Compound Name"
mzExpectTitle = "m/z (Expected)"

compoundNames = set()
for currSheetName in sheetNames:
    sheetData = screenDataBook[currSheetName]
    compoundNameData  = sheetData[compoundNameTitle]
    print currSheetName, ": ", compoundNameData
    #unique compund names from each sheet data
    for name in compoundNameData:
        compoundNames.add(name)



print "Final CompundNames: ", compoundNames
print "len = %d " % len(compoundNames)

#Append compound name data to first column of Sheet-1
compoundNames = list(compoundNames)
compoundNames.sort()
sheetOne = newScreenBook.create_sheet("Sheet-1", 0)
sheetOne.append([compoundNameTitle, mzExpectTitle])
writeDataToColumn(newScreenBook, "Sheet-1", compoundNames, 1)

#start to append m/z (expected) data to Sheet-1
mzInfo = extractMZExpectData(screenDataBook)
mzInfoList = []
for compoundName in compoundNames:
    mzExpectValue = mzInfo.get(compoundName)
    mzInfoList.append(mzExpectValue)

print "mzInfo: ", mzInfo
print "mzInfoListLen = ", len(mzInfoList)

writeDataToColumn(newScreenBook, "Sheet-1", mzInfoList, 2)




writeWordBook(newScreenBook, "screen-filter.xlsx")



exit
excelProcess = popen4("start excel D:/workspace/screen-filter.xlsx")
print("Enter to finish")
#line = sys.stdin.readline()
sleep(100)
Popen("taskkill /F /im EXCEL.EXE",shell=True)


