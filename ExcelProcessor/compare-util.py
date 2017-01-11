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
from Logger import MyLogger
from Logger import logging

fileName = "./analysis/lipid1.xlsx"
logger = MyLogger("compare-Logger", logging.INFO).getLogger()
dataBook = loadData(fileName, logger)

sheetNames = list(dataBook)
logger.info("sheetNames = " + sheetNames)

sheet1 = dataBook["Sheet-1"]

lipidNames = sheet1["Lipid"]

i = 0
for n in lipidNames:
    i = i + 1
    logger.info(str(i) + ":" + n)


logger.info("size = " + len(lipidNames))


