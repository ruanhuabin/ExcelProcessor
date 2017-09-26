from openpyxl import Workbook
from openpyxl import load_workbook
import time
import math
from Logger2 import MyLogger
import sys
logger = MyLogger().getLogger()
def loadData(fileName):
    logger.info("Start loading data: " + fileName)
    wholeWorkBook = {}
    inputDataDict = load_workbook(fileName)
    logger.info("Finish loading data: " + fileName)
    
    sheetNames = inputDataDict.get_sheet_names()
    sheetNames.sort()   
    logger.info("sheet names: " + str(sheetNames))
    for currentSheetName in sheetNames:
        logger.info("Start to load sheet data: " + currentSheetName)
        sheetData = inputDataDict.get_sheet_by_name(currentSheetName)
        rows = sheetData.rows;
        columns = sheetData.columns;

        sheetRowDataDict = {}
        rowValue = []
        for row in rows:
            for v in row:
                rowValue.append(v.value)

            #logger.info("row: " + str(rowValue))
            sheetRowDataDict[rowValue[0]] = rowValue[1:]
        wholeWorkBook[currentSheetName] = sheetRowDataDict
            #sheetRowDataDict[row[0].value] = [v.value for v in row[0:]]
        #logger.info("row data:{0} ==>{1}".format(row[0].value, sheetRowDataDict[row[0].value]))
    return wholeWorkBook


if __name__ == "__main__":
    wb = loadData(sys.argv[1])
    for(k, v) in wb.iteritems():
        logger.info("data in {0}".format(k))
        for(k1, v1) in v.iteritems():
            logger.info("{0}-->{1}".format(k1, v1))
