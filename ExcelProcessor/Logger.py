# encoding: utf-8

'''
Created on 2016��9��15��

@author: ruanhuabin
'''
import logging

class MyLogger(object):
    
    def __init__(self, loggerName, loggerLevel=logging.DEBUG):
        self.logger = logging.getLogger(loggerName)
        self.logger.setLevel(logging.DEBUG)
        
        consoleHandler = logging.StreamHandler()
        consoleHandler.setLevel(loggerLevel) 
        
        formatter = logging.Formatter("%(asctime)s-[ %(levelname)s ]: %(message)s")
        
        consoleHandler.setFormatter(formatter)
        
        self.logger.addHandler(consoleHandler)
        
    def getLogger(self):
        return self.logger
        


def runLoggerTest():
    logger = MyLogger("Simple_Logger").getLogger()
    
    logger.debug("This is debug message")
    logger.info("This is info message")
    logger.warning("This is a warn message")
    logger.error("This is a error message")
    logger.critical("This is a critical message")

def runGetTimeTest():
    import time
    
    st = time.localtime()
    year = st.tm_year
    month = st.tm_mon
    day = st.tm_mday
    hour = st.tm_hour
    min = st.tm_min
    sec = st.tm_sec
    
    strTime = str(year) + "-" + str("%02d" % month) + "-" + str("%02d" % day) + "-" + str("%02d" % hour) + ":" + str("%02d" % min) + ":" + str("%02d" % sec)
    print strTime
    

    print time.localtime()
       
        
if __name__ == '__main__':
    #runLoggerTest()
    #runGetTimeTest()
    pass