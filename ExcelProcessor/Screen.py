#!/usr/bin/env python
# encoding: utf-8
#from util import writeWordBook, createOutputWordBook, writeDataToColumn, extractMZExpectData,\
#    loadData

from util import writeWordBook, createOutputWordBook, writeDataToColumn, extractMZExpectData, loadData,\
    extractLSMARTData, isAllNA, extractCPLSData, extractIPData, isContainPass,\
    extractLSData, extractRTMeasuredData, extractMZDeltaData,\
    extractMeasuredAreaData, printDict, writeDataToRow, extractALLRTMeasuredData,\
    highLightCell, checkFileValid
from subprocess import Popen
from popen2 import popen4
from os import system
from time import time, sleep
from constant import *
from __builtin__ import sorted
import operator
import inspect
import sys

def init(src, logger):

    newScreenBook = createOutputWordBook()
    screenDataBook = loadData(src)
    sheetNames = list(screenDataBook)
    sheetNames.sort()
    #print sheetNames
    #print len(sheetNames)
    logger.info("Sheet names [ %s ] in file [%s]" % (str(sheetNames), src))
    sheetOne = newScreenBook.create_sheet("Sheet-1", 0)
    sheetTwo = newScreenBook.create_sheet("Sheet-2", 1)
    
    return [screenDataBook, newScreenBook]

def extractCompoundNameColumn(screenDataBook, newScreenBook, logger):
    sheetNames = list(screenDataBook)
    sheetNames.sort()

    compoundNames = set()
    for currSheetName in sheetNames:
        sheetData = screenDataBook[currSheetName]
        compoundNameData  = sheetData[compoundNameTitle]
        #print currSheetName, ": ", compoundNameData
        logger.debug("Current sheet name %s : include compound name [%s]" % (currSheetName, str(compoundNameData)))
        
        #unique compund names from each sheet data
        for name in compoundNameData:
            compoundNames.add(name)
    
    
    
    #print "Final CompundNames: ", compoundNames
    #print "len = %d " % len(compoundNames)
    logger.info("After remove duplicated compound names, the final compound names are: [%s]" % (str(compoundNames)))
    #Append compound name data to first column of Sheet-1
    compoundNames = list(compoundNames)
    compoundNames.sort()
#     sheetOne = newScreenBook.create_sheet("Sheet-1", 0)
#     sheetTwo = newScreenBook.create_sheet("Sheet-2", 0)
    sheetOne = newScreenBook.get_sheet_by_name("Sheet-1")
    sheetTwo = newScreenBook.get_sheet_by_name("Sheet-2")
    #Append title
    sheetOneRowTitle = [compoundNameTitle, mzExpectedTitle, rtMeasuredTitle, libraryScoreTitle, ipTitle, lsTitle, rtRangeTitle, mzDeltaTitle]
    sheetOne.append(sheetOneRowTitle)
    sheetTwo.append(sheetOneRowTitle)
    writeDataToColumn(newScreenBook, "Sheet-1", compoundNames, 1, 2)
    writeDataToColumn(newScreenBook, "Sheet-2", compoundNames, 1, 2)
    
    return compoundNames

#start to append m/z (expected) data to Sheet-1
def extractMZExpectColumn(screenDataBook, compoundNames, newScreenBook, logger):

    mzInfo = extractMZExpectData(screenDataBook)
    mzInfoList = []
    for compoundName in compoundNames:
        mzExpectValue = mzInfo.get(compoundName)
        mzInfoList.append(mzExpectValue)
    
    #print "mzInfo: ", mzInfo
    #print "mzInfoListLen = ", len(mzInfoList)
    logger.info("mz info is: [num = %d], [%s]" % (len(mzInfoList), str(mzInfo)))
    
    writeDataToColumn(newScreenBook, "Sheet-1", mzInfoList, 2, 2)
    writeDataToColumn(newScreenBook, "Sheet-2", mzInfoList, 2, 2)

#Start to extract RT Value

g_rtValue=[]
def genRTColumn(screenDataBook, compoundNames, newScreenBook, logger):
    lsmartInfo = extractLSMARTData(screenDataBook)
    print lsmartInfo
    cpNames = list(lsmartInfo)
    print cpNames
    print len(cpNames)
    
    cpNames.sort()
    cprtInfo = []
    for currCPName in cpNames:
        lsmartValue = lsmartInfo.get(currCPName)
        
        #print currCPName, ":"
        logger.info("Current compound name: %s" % currCPName)
        lsInfo = []
        maInfo = []
        for currLSMARTValue in lsmartValue:
            #print currLSMARTValue
            mzDeltaValue = currLSMARTValue[1]
            lsInfo.append(mzDeltaValue)
            maValue = currLSMARTValue[2]
            maInfo.append(maValue)
        #print lsInfo
        #print isAllNA(lsInfo)
        #print maInfo
        
        logger.info("library score info: [%s]" % (str(lsInfo)))
        logger.info("measured area info: [%s]" % (str(maInfo)))
        
        isAllNAValue = isAllNA(lsInfo)
        if(isAllNAValue == False):
            sortLSMARTValue = sorted(lsmartValue, key = operator.itemgetter(1), reverse = True)
            #sorted(data.iteritems(),key=operator.itemgetter(1,0),reverse=True)
        else:
            sortLSMARTValue = sorted(lsmartValue, key = operator.itemgetter(2), reverse = True)
         
        #print lsmartValue   
        #print sortLSMARTValue
        
        logger.info("lsmartValue: [%s]" % (str(lsmartValue)))
        logger.info("sortLSMARTValue: [%s]" % (str(sortLSMARTValue)))
        
        cprtInfo.append(sortLSMARTValue[0][3])
    #print cprtInfo
    logger.info("cprtInfo: [%s]" % (str(cprtInfo)))
    writeDataToColumn(newScreenBook, "Sheet-1", cprtInfo, 3, 2)
    writeDataToColumn(newScreenBook, "Sheet-2", cprtInfo, 3, 2)
    
    #copy rtvalue to g_rtValue for the purpose of making highling of sheet2
    for v in cprtInfo:
        g_rtValue.append(v)

#start to extract library score



def genLibraryScoreColumn(screenDataBook, compoundNames, newScreenBook, logger):
    cplsInfo = extractCPLSData(screenDataBook)
    print "cplsInfo: ", cplsInfo
    logger.info("cplsInfo: [%s]" % (str(cplsInfo)))
    cpNames = list(cplsInfo)
    cpNames.sort()
    lsFinalInfo = []
    for currCPName in cpNames:
        mzDeltaValue = cplsInfo[currCPName]
        lsInfo = []
        newLSInfo = []
        for i in range(len(mzDeltaValue)):
            lsInfo.append(mzDeltaValue[i][1])
            
        isAllNAValue = isAllNA(lsInfo)
        
        lsFinalValue = "N/A"
        if(isAllNAValue == False):
            lsInfo.sort(cmp=None, key=None, reverse=True)
            lsFinalValue = lsInfo[0]
            
        #print currCPName, ":", lsInfo
        logger.info("currCPName: [%s], lsInfo : [%s]" % (str(currCPName), str(lsInfo)))
        
        lsFinalInfo.append(lsFinalValue)
    
    print lsFinalInfo
    logger.info("lsFinalInfo: [%s]" % (str(lsFinalInfo)))
    
    writeDataToColumn(newScreenBook, "Sheet-1", lsFinalInfo, 4, 2)
    writeDataToColumn(newScreenBook, "Sheet-2", lsFinalInfo, 4, 2)
    
def genIPColumn(screenDataBook, compoundNames, newScreenBook, logger):
    ipInfoDict = extractIPData(screenDataBook)
    #print "ipInfoList = ", ipInfoDict
    logger.info("ipInfoDict: [%s]" % (str(ipInfoDict)))
    cpNames = list(ipInfoDict)
    cpNames.sort()
    
    
    ipFinalInfo = []
    
    for currCPName in cpNames:
        ipValue = ipInfoDict[currCPName]
        ipInfoList = []
        #print currCPName, ":",
        for i in range(len(ipValue)):
            ipInfoList.append(ipValue[i][1])
        flag = isContainPass(ipInfoList)
        
        if(flag == True):
            ipFinalInfo.append("Pass")
        else:
            ipFinalInfo.append("Fail")
        
        #print ipInfoList
        logger.info("compound name = %s, ipInfoList = [%s]" %(currCPName, str(ipInfoList)))
    
    #print "IP Final Info: " , ipFinalInfo
    logger.info("IP Final Info: %s" %(str(ipFinalInfo)))
    writeDataToColumn(newScreenBook, "Sheet-1", ipFinalInfo, 5, 2)
    writeDataToColumn(newScreenBook, "Sheet-2", ipFinalInfo, 5, 2)
    
    
def genLSColumn(screenDataBook, compoundNames, newScreenBook, logger):
    lsInfoDict = extractLSData(screenDataBook)
    logger.info("lsInfoList = [%s]" % str(lsInfoDict))
    cpNames = list(lsInfoDict)
    cpNames.sort()
    logger.info("cpNames = %s" %(str(cpNames)))
    
    lsFinalInfo = []
    
    for currCPName in cpNames:
        mzDeltaValue = lsInfoDict[currCPName]
        lsInfoList = []
        #print currCPName, ":",
        for i in range(len(mzDeltaValue)):
            lsInfoList.append(mzDeltaValue[i][1])
        flag = isContainPass(lsInfoList)
        
        if(flag == True):
            lsFinalInfo.append("Pass")
        else:
            lsFinalInfo.append("Fail")
        
        #print lsInfoList
        logger.info("compound name = %s, lsInfoList: [%s]" % (currCPName, str(lsInfoList)))
    
    #print "LS Final Info: " , lsFinalInfo
    logger.info("lsFinalInfo: [%s]" % (str(lsFinalInfo)))
    writeDataToColumn(newScreenBook, "Sheet-1", lsFinalInfo, 6, 2)
    writeDataToColumn(newScreenBook, "Sheet-2", lsFinalInfo, 6, 2)
    
def genRTRangeColumn(screenDataBook, compoundNames, newScreenBook, logger):
    rtMeasuredInfoDict = extractRTMeasuredData(screenDataBook)
    #print "rtMeasuredInfoList = ", rtMeasuredInfoDict
    logger.info("rtMeasuredInfoList: [%s]" % (str(rtMeasuredInfoDict)))
    cpNames = list(rtMeasuredInfoDict)
    cpNames.sort()
    #print "cpNames = ", cpNames
    
    rtMeasuredFinalInfo = []
    
    for currCPName in cpNames:
        mzDeltaValue = rtMeasuredInfoDict[currCPName]
        rtMeasuredInfoList = []
       # print currCPName, ":",
        for i in range(len(mzDeltaValue)):
            rtMeasuredInfoList.append(mzDeltaValue[i][1])
        
        rtMeasuredInfoList.sort()
        
        #print rtMeasuredInfoList
        logger.info("currCPName = %s, rtMeasuredInfoList: [%s]" % (currCPName, str(rtMeasuredInfoList)))
        
        rangeValue = rtMeasuredInfoList[-1] - rtMeasuredInfoList[0]
        #rtMeasuredFinalInfo.append([currCPName, rangeValue])
        rtMeasuredFinalInfo.append(rangeValue)
    
    #print "RT Range Final Info: " , rtMeasuredFinalInfo
    logger.info("RT Range Final Info: : [%s]" % (str(rtMeasuredFinalInfo)))
    writeDataToColumn(newScreenBook, "Sheet-1", rtMeasuredFinalInfo, 7 , 2)
    writeDataToColumn(newScreenBook, "Sheet-2", rtMeasuredFinalInfo, 7 , 2)


def genMZDeltaColumn(screenDataBook, compoundNames, newScreenBook, logger):
    mzDeltaInfoDict = extractMZDeltaData(screenDataBook)
    #print "MZDeltaInfoList = ", mzDeltaInfoDict
    logger.info("MZDeltaInfoList: [%s]" % ( str(mzDeltaInfoDict)))
    cpNames = list(mzDeltaInfoDict)
    cpNames.sort()
    
    
    mzDeltaFinalInfo = []
    
    for currCPName in cpNames:
        mzDeltaValue = mzDeltaInfoDict[currCPName]
        mzDeltaInfoList = []
        #print currCPName, ":",
        for i in range(len(mzDeltaValue)):
            mzDeltaInfoList.append(mzDeltaValue[i][1])
                       
        #print mzDeltaInfoList
        
        logger.info("currCPName = %s, mzDeltaInfoList: [%s]" % (currCPName, str(mzDeltaInfoList)))
        
        averageValue = float(sum(mzDeltaInfoList)) / len(mzDeltaInfoList)
        #mzDeltaFinalInfo.append([currCPName, averageValue])
        mzDeltaFinalInfo.append(averageValue)
    
    print "MZ Delta Final Info: " , mzDeltaFinalInfo
    logger.info("MZ Delta Final Info: " + str(mzDeltaFinalInfo))
    writeDataToColumn(newScreenBook, "Sheet-1", mzDeltaFinalInfo, 8, 2)
    writeDataToColumn(newScreenBook, "Sheet-2", mzDeltaFinalInfo, 8, 2)

def getKey(item):
    return item[0]
   
def genMeasuredAreaColumn(screenDataBook, compoundNames, newScreenBook, logger):
    measuredAreaInfoDict = extractMeasuredAreaData(screenDataBook)
    #print "measuredAreaInfoDict = ", measuredAreaInfoDict
    
    logger.info("measuredAreaInfoDict = " + str(measuredAreaInfoDict))
    cpNames = list(measuredAreaInfoDict)
    cpNames.sort()
    
    
    sheetNames = list(screenDataBook)
    sheetNames.sort()
    #Append sheet name to first row
    writeDataToRow(wordBook=newScreenBook, sheetName="Sheet-1", data = sheetNames, rowIndex = 1, columnStartIndex = 9)
    #printDict(measuredAreaInfoDict)

    nextRowIndex = 2
    for currCPName in cpNames:
        snmaValues = measuredAreaInfoDict[currCPName]
        snmaValues.sort(key=getKey)
        #print currCPName, ":"
        #print ">>: ", snmaValues
        logger.info("current compound name = %s, snmaValues = %s" %(currCPName, snmaValues))
        maValues = []
        for[sn, ma] in snmaValues:
            maValues.append(ma)
        
        writeDataToRow(newScreenBook, "Sheet-1", maValues, nextRowIndex, 9 )
        nextRowIndex = nextRowIndex + 1
        
        
        
    #print sheetNames
    
    
def genRTMeasuredColumn(screenDataBook, compoundNames, newScreenBook, logger):
    rtMeasuredInfoDict = extractALLRTMeasuredData(screenDataBook)
    print "rtMeasuredInfoDict = ", rtMeasuredInfoDict
    logger.info("rtMeasuredInfoDict = " + str(rtMeasuredInfoDict))
    cpNames = list(rtMeasuredInfoDict)
    cpNames.sort()
    #print "cpNames = ", cpNames
    
    sheetNames = list(screenDataBook)
    sheetNames.sort()
    #Append sheet name to first row
    writeDataToRow(wordBook=newScreenBook, sheetName="Sheet-2", data = sheetNames, rowIndex = 1, columnStartIndex = 9)
    #printDict(rtMeasuredInfoDict)

    nextRowIndex = 2
    rtIndex = 0
    for currCPName in cpNames:
        snrtmValues = rtMeasuredInfoDict[currCPName]
        snrtmValues.sort(key=getKey)
        #print currCPName, ":"
        #print ">>: ", snrtmValues
        
        logger.info("Current compound name = %s, snrtmValues = %s" %(currCPName, snrtmValues))
        maValues = []
        for[sn, ma] in snrtmValues:
            maValues.append(ma)
        
        writeDataToRow(newScreenBook, "Sheet-2", maValues, nextRowIndex, 9 )       
        highLightCell(newScreenBook, "Sheet-2", g_rtValue[rtIndex], maValues, nextRowIndex, 9 )
        nextRowIndex = nextRowIndex + 1
        rtIndex = rtIndex + 1
        
        
        
    print sheetNames
        

rowTitleMust = [compoundNameTitle, mzExpectedTitle, libraryScoreTitle, measuredAreaTitle, ipTitle, lsTitle, rtMeasuredTitle, mzDeltaTitle]


# [screenDataBook, newScreenBook] = init(src="small-screen.xlsx")
# [missingNum, missingRowTitleDict] = checkFileValid(screenDataBook, rowTitleMust)
# if(missingNum > 0):
#     print "Error: Some worksheet missing some column(s):"
#     printDict(missingRowTitleDict)    
#     raise ValueError("Error: Some worksheet missing some column(s), see missing column above")
# compoundNames = extractCompoundNameColumn(screenDataBook, newScreenBook)
#  
# # 
# extractMZExpectColumn(screenDataBook, compoundNames, newScreenBook)       
# genRTColumn(screenDataBook, compoundNames, newScreenBook)   
# genLibraryScoreColumn(screenDataBook, compoundNames, newScreenBook)
# genIPColumn(screenDataBook, compoundNames, newScreenBook)
# genLSColumn(screenDataBook, compoundNames, newScreenBook)
# genRTRangeColumn(screenDataBook, compoundNames, newScreenBook)
# genMZDeltaColumn(screenDataBook, compoundNames, newScreenBook)
#  
# genMeasuredAreaColumn(screenDataBook, compoundNames, newScreenBook)
# genRTMeasuredColumn(screenDataBook, compoundNames, newScreenBook)
# 
# writeWordBook(newScreenBook, "screen-filter.xlsx")
# 
# 
# 
# excelProcess = popen4("start excel D:\workspace-excelprocess-final\ExcelProcessor/screen-filter.xlsx")
# print("Enter to finish")
# import sys
# line = sys.stdin.readline()
# #sleep(100)
# Popen("taskkill /F /im EXCEL.EXE",shell=True)

