# encoding: utf-8
from Logger import MyLogger
import logging
import math
import re
import pprint
#import operator

logger = MyLogger("Lipid-Logger", logging.INFO).getLogger()
ms2Window = 0.2
topRTRange = 0.25
#保存合并后的名字与原始名字的映射
lipidAlias = {}

def makeTestData():
    dataBook = {}
    fileBook1 = {}
    fileBook2 = {}
    
    fileBook3 = {}
    fileBook4 = {}
    fileBook5 = {}
    fileBook6 = {}
    fileBook7 = {}
    
    
    fileBook1["LipidIon"] = ["ChE(18:3)+H", "ChE(20:5)+NH4", "ChE(20:5)+H", "ChE(22:4)+NH4", "ChE(20:5)+H"]
    fileBook1["Rt"] = ["10.1", "10.2", "10.3","10.4", "11.80"]
    fileBook1["TopRT"] = ["10.25", "10.42", "10.45", "10.88", "11.64"]
    fileBook1["Formula"] = ["fm1", "fm2", "fm2", "fm2", "fm2"]
    fileBook1["Grade"] = ["A", "A", "B", "B", "D"]
    fileBook1["ObsMz"] = ["OM1", "OM2", "OM3", "OM4", "OM5"]
    fileBook1["Area"] = ["Area1", "Area2", "Area3", "Area4", "Area5"]
    
    fileBook2["LipidIon"] = ["NE(18:3)+H", "ChE(20:5)+NH4", "NE(20:5)+H", "ChE(22:4)+NH4", "ChE(20:5)+H"]
    fileBook2["Rt"] = ["10.1", "10.2", "10.3","10.4", "10.4"]
    fileBook2["TopRT"] = ["10.25", "10.42", "10.45", "10.92", "10.55"]
    fileBook2["Formula"] = ["fm1", "fm2", "fm2", "fm2", "fm2"]
    fileBook2["Grade"] = ["A", "D", "C", "D", "B"]
    fileBook2["ObsMz"] = ["OM1", "OM2", "OM3", "OM4", "OM5"]
    fileBook2["Area"] = ["Area1", "Area2", "Area3", "Area4", "Area5"]
    
    
    fileBook3["LipidIon"] = ["TG(4:0/16:0/22:5)+NH4", "TG(4:0/22:5/16:0)+NH4", "DG(16:0/4:0/22:5)+NH4", "DG(4:0/16:0/22:5)+NH4", "TG(4:0/16:0/28:4)+NH4"]
    fileBook3["Rt"] = ["10.1", "10.2", "10.3","10.4", "10.5"]
    fileBook3["TopRT"] = ["10.1", "10.2", "10.3", "10.4", "10.5"]
    fileBook3["Formula"] = ["fm2", "fm2", "fm2", "fm2", "fm2"]
    fileBook3["Grade"] = ["A", "D", "C", "D", "B"]
    fileBook3["ObsMz"] = ["OM1", "OM2", "OM3", "OM4", "OM5"]
    fileBook3["Area"] = ["Area1", "Area2", "Area3", "Area4", "Area5"]
    
    fileBook4["LipidIon"] = ["PC(16:0e/22:5)+NH4", "PC(22:5/16:0e)+NH4", "SM(16:0/4:0p)+NH4", "SM(4:0p/16:0)+NH4", "PC(d16:0/28:4+O)+NH4", "SM(16:0/4:0p)+NH4"]
    fileBook4["Rt"] = ["10.1", "10.2", "10.3","10.4", "10.5", "10.8"]
    fileBook4["TopRT"] = ["10.1", "10.2", "10.3", "10.4", "10.5", "10.8"]
    fileBook4["Formula"] = ["fm3", "fm3", "fm3", "fm3", "fm3", "fm3"]
    fileBook4["Grade"] = ["A", "D", "C", "D", "B", "A"]
    fileBook4["ObsMz"] = ["OM1", "OM2", "OM3", "OM4", "OM5", "OM6"]
    fileBook4["Area"] = ["Area1", "Area2", "Area3", "Area4", "Area5", "Area6"]
    
    fileBook5["LipidIon"] = ["Cer(16:0e/22:5)+NH4", "Cer(22:5e/16:0)+NH4", "phSM(16:0/4:0p)+NH4", "phSM(4:0p/16:0)+NH4", "Cer(16:0e/22:5)+NH4", "phSM(16:0/4:0p)+NH4", "phSM(16:0/4:0p)+NH4"]
    fileBook5["Rt"] = ["10.1", "10.2", "10.3","10.4", "10.5", "10.8", "10.4"]
    fileBook5["TopRT"] = ["10.1", "10.2", "10.3", "10.4", "10.5", "10.8", "10.4"]
    fileBook5["Formula"] = ["fm5", "fm5", "fm5", "fm5", "fm5", "fm5", "fm5"]
    fileBook5["Grade"] = ["A", "B", "B", "A", "B", "A", "B"]
    fileBook5["ObsMz"] = ["OM1", "OM2", "OM3", "OM4", "OM5", "OM6", "OM7"]
    fileBook5["Area"] = ["Area1", "Area2", "Area3", "Area4", "Area5", "Area6", "Area7"]
    
    #注意：不可能出现两盒化合物名称相同，但是formula不同的情况，在构造测试数据的时候特别注意
    fileBook6["LipidIon"] = ["CerG1(16:0e/22:5)+NH4", "CerG1(22:5e/16:0)+NH4", "phSMG2(16:0/4:0p)+NH4", "phSMG2(4:0p/16:0)+NH4", "CerG1(16:0e/22:5)+NH4", "phSMG2(16:0/4:0p)+NH4", "phSMG2(16:0/4:0p)+NH4"]
    fileBook6["Rt"] = ["10.1", "10.2", "10.3","10.4", "10.5", "10.8", "10.4"]
    fileBook6["TopRT"] = ["10.1", "10.2", "10.3", "10.4", "10.5", "10.8", "10.4"]
    fileBook6["Formula"] = ["fm6", "fm6", "fm6", "fm6", "fm6", "fm6", "fm6"]
    fileBook6["Grade"] = ["C", "D", "D", "C", "D", "C", "D"]
    fileBook6["ObsMz"] = ["OM1", "OM2", "OM3", "OM4", "OM5", "OM6", "OM7"]
    fileBook6["Area"] = ["Area1", "Area2", "Area3", "Area4", "Area5", "Area6", "Area7"]
    
    
    fileBook7["LipidIon"] = ["CerG2(16:0e/22:5)+NH4", "CerG2(22:5e/16:0)+NH4", "phSMG3(16:0/4:0p)+NH4", "phSMG3(4:0p/16:0)+NH4", "CerG2(16:0e/22:5)+NH4", "phSMG3(16:0/4:0p)+NH4", "phSMG3(4:0p/16:0)+NH4"]
    fileBook7["Rt"] = ["10.1", "10.2", "10.3","10.4", "10.5", "10.8", "10.4"]
    fileBook7["TopRT"] = ["10.1", "10.2", "10.3", "10.4", "10.5", "10.8", "10.4"]
    fileBook7["Formula"] = ["fm7", "fm7", "fm7", "fm7", "fm7", "fm7", "fm7"]
    fileBook7["Grade"] = ["A", "D", "D", "C", "C", "B", "A"]
    fileBook7["ObsMz"] = ["OM1", "OM2", "OM3", "OM4", "OM5", "OM6", "OM7"]
    fileBook7["Area"] = ["Area1", "Area2", "Area3", "Area4", "Area5", "Area6", "Area7"]
    
    
    dataBook["f1"] = fileBook1;
    dataBook["f2"] = fileBook2;
    dataBook["f3"] = fileBook3;
    dataBook["f4"] = fileBook4;
    dataBook["f5"] = fileBook5;
    dataBook["f6"] = fileBook6;
    dataBook["f7"] = fileBook7;
    
    
    return dataBook        

#将样品数据组织成五元组的形式(lipidIons, Rts, TopRTs, diff, Formulas, Grades)        
def makeTuple(dataBook):
    logger.info("Start to make databook as tuple list")    
    lipidInfo = []    
    files = list(dataBook)
    for f in files:
        fileData = dataBook[f]
        lipidIons = fileData["LipidIon"]
        Rts = fileData["Rt"]
        TopRTs = fileData["TopRT"]
        Formulas = fileData["Formula"]
        Grades = fileData["Grade"]
        ObsMz = fileData["ObsMz"]
        Area = fileData["Area"]
        
        logger.info("lipidIons:" + str(lipidIons)) 
        logger.info("Rts:" + str(Rts))
        logger.info("TopRTs:" + str(TopRTs))
        logger.info("Formulas:" + str(Formulas))
        logger.info("Grades:" + str(Grades))
        logger.info("obsMz:" + str(ObsMz))
        logger.info("--------------------------------------------------------------")
        
        columnDataSize = len(lipidIons)
        for i in range(columnDataSize):
            diff = math.fabs(float(Rts[i]) - float(TopRTs[i]))
            li = (lipidIons[i], Rts[i], TopRTs[i], diff, Formulas[i], Grades[i], ObsMz[i], Area[i],f)
            lipidInfo.append(li)
    
    #lipidInfo = sorted(lipidInfo,key=operator.itemgetter(3,0),reverse=False)            
    logger.info("End to make databook as tuple list")    
    return lipidInfo     

#在lipidInfo中删除RT和TopRT差值大于0.2的元组
def rm0dot2(lipidInfo):
    
    logger.info("Start to remove item that the gap between RT and TopRT is bigger than ms2Window(0.2)")
    newLipidInfo = []
    for item in lipidInfo:
        diff = item[3]
        if(diff <= ms2Window):
            newLipidInfo.append(item)
    
    logger.info("End to remove item that the gap between RT and TopRT is bigger than ms2Window(0.2)")
    
    return newLipidInfo


#计算每一种化合物在所有文件中的TopRT的平均值
def calTopRTAvg(lipidInfo):
    avgTable = {};
    topRTTable = {}
    for item in lipidInfo:
        lipidName = item[0]
        topRT = item[2]
        
        if(topRTTable.has_key(lipidName)):
            topRTTable[lipidName].append(float(topRT))
        else:
            topRTTable[lipidName] = [float(topRT)]


    logger.info("topRT Table = " + str(topRTTable))
    
    for(k, v) in topRTTable.iteritems():
        if(len(v) == 0):
            avgTable[k] = 0.0
        else:
            avgTable[k] = sum(v)/len(v)
        
    logger.info("avg Table = " + str(avgTable))
    return (avgTable, topRTTable)

#拿到所有相同formula对应的set(化合物),具有相同formula的化合物可以通过topRTTable这个dict来取得其所有的topRT值
def getFormulaMap(lipidInfo):
    
    logger.info("Start to get lipid names with same formula")
    #保存f->c的映射
    f2c = {}
    #保存c->f的映射
    c2f = {}
    
    
    
    for item in lipidInfo:
        formula = item[4]
        lipidName = item[0]
        #topRT = item[2]
        if(f2c.has_key(formula)):            
            f2c[formula].add(lipidName)            
        else:
            f2c[formula] = set([lipidName])
        
        if(c2f.has_key(lipidName)):
            c2f[lipidName].add(formula)
        else:
            c2f[lipidName] = set([formula])
            
    
    logger.info("end to get lipid names with same formula")
    return (f2c,c2f)

def getObsMZMap(lipidInfo):
    
    logger.info("Start to get lipid name mapping to obsmz info")
    #保存c->f的映射
    c2om = {}    
    for item in lipidInfo:
        obsMZ = item[6]
        lipidName = item[0]
       
        
        if(c2om.has_key(lipidName)):
            c2om[lipidName].add(obsMZ)
        else:
            c2om[lipidName] = set([obsMZ])
            
    
    logger.info("End to get lipid name mapping to obsmz info")
    return c2om
               
#获取化合物括号部分数字对的个数。
def getGroupNum(compndName):
    
    parenthesesPart = re.search('\(.*\)', compndName).group();   
    #print("parenthesesPart = " + str(parenthesesPart))
    semicolon = re.findall(':', str(parenthesesPart))  
    
    #print("semicolon = " + str(semicolon))    
    
    return len(semicolon)
#提取符合条件2.1的(化合物,toprt)，同时将该化合物信息从候选的lipidInfo中剔除
def p2dot1(f2c, c2TopRTAvg, c2TopRT):
    
    
    logger.info("Start to process lipid info with only one group num")
    vldLipidInfo = []
    
    
    for (k, v) in f2c.iteritems():
        lipidNames = list(v)
        for n in lipidNames:
            grpNum = getGroupNum(n)
            if(grpNum > 1):
                continue
            
            #处理只有1组数字对的情况
            lipidAvg = c2TopRTAvg[n]
            topRTs = c2TopRT[n]
            
            #保存需要重新计算平均值的topRT值
            mergeValues = []
            #保存需要单独保存的topRT值
            unMergeValues = []
            for topRT in topRTs:
                diff = math.fabs(topRT - lipidAvg)
                
                if(diff <= topRTRange):
                    mergeValues.append(topRT)
                else:
                    unMergeValues.append(topRT)
            
            if(len(mergeValues) >= 1):
                newAvg = sum(mergeValues) / len(mergeValues)
                vldLipidInfo.append((n, newAvg))
            
            for value in unMergeValues:
                vldLipidInfo.append((n, value))
                    
                    
    logger.info("End to process lipid info with only one group num")                
    return vldLipidInfo        
        
#拿到化合物括号中的数字对等信息
def getInfoInPare(lipidName):
    parenthesesPart = re.search('\(.*\)', lipidName).group();
    parenthesesPart = str(parenthesesPart)
    parenthesesPart = parenthesesPart[1:len(parenthesesPart) - 1]    
    logger.info("parenthesesPart = " + parenthesesPart)    
    elems = re.split('\+|/', parenthesesPart)    
    logger.info("elems = " + str(elems))
    
    elems = sorted(elems)
    return elems 

#将化合物括号部分的数字对按照升序重新组合
def renameLipid(lipidName):
    prefix = lipidName[0:2]    
    elems = getInfoInPare(lipidName)
    newPare = '/'.join(elems)
    newPare = "(" + newPare + ")"
    suffix = lipidName[lipidName.find(')') + 1:]
    newLipidName = prefix + newPare + suffix
    
    
    #只要被调用一次，就需要保存一次新名字到原始名字的映射
    if(lipidAlias.has_key(newLipidName)):
        lipidAlias[newLipidName].add(lipidName)
    else:
        lipidAlias[newLipidName] = set([lipidName])
    
    return newLipidName
      
#将DG，TG开头的化合物中间的数字部分重新按照升序排列，以便于发现相同的化合物
def reorderDGTG(c2TopRT):
    
    logger.info("Start to reorder the lipid-->toprts pair with the lipid name start with DG, TG")
    #newc2TopRT中，key保存以DG，TG开头，括号部分经过排序的化合物，value是化合物名称经过处理后是相同的化合物的所有的topRT值
    newc2TopRT = {}
    newc2TopRTAvg = {}
    for (k,v)in c2TopRT.iteritems():
        prefix = k[0:2]
        if(prefix != "DG" and prefix != "TG"):            
            continue;
        
        topRTs = c2TopRT[k]
        
#         elems = getInfoInPare(k)
#         newPare = '/'.join(elems)
#         newPare = "(" + newPare + ")"
#         suffix = k[k.find(')') + 1:]
#         newLipidName = prefix + newPare + suffix

        newLipidName = renameLipid(k)
        
        if(newc2TopRT.has_key(newLipidName)):
            for topRT in topRTs:
                newc2TopRT[newLipidName].append(topRT)
        else:   
                newc2TopRT[newLipidName] = topRTs
        
    
    for (k,v) in newc2TopRT.iteritems():
        if(len(v) == 0):
            newc2TopRTAvg[k] = 0.0
        else:
            newc2TopRTAvg[k] = sum(v)/len(v)
            
    
    logger.info("End to reorder the lipid-->toprts pair with the lipid name start with DG, TG")
    return (newc2TopRTAvg, newc2TopRT)
        
            
        
                
def p2dot2(f2c, c2TopRT):
    
    logger.info("Start to process lipid info with lipid name start with DG, TG")
    vldLipidInfo = []
    (newc2TopAvg, newc2TopRT) = reorderDGTG(c2TopRT)
    for(k,v) in f2c.iteritems():
        lipidNames = list(v)
        
        for n in lipidNames:
            prefix = n[0:2]
            #只处理DG或者TG开头的
            if(prefix != "DG" and prefix != "TG"):
                continue
            newLipidName = renameLipid(n)
            
            topRTs = newc2TopRT[newLipidName]
            lipidAvg = newc2TopAvg[newLipidName]
            
            print("newlipidName" + newLipidName)
            print("topRTs" + str(topRTs))
            print("lipidAvg" + str(lipidAvg))
            
            #保存需要重新计算平均值的topRT值
            mergeValues = []
            #保存需要单独保存的topRT值
            unMergeValues = []
            for topRT in topRTs:
                diff = math.fabs(topRT - lipidAvg)
                
                if(diff <= topRTRange):
                    mergeValues.append(topRT)
                else:
                    unMergeValues.append(topRT)
            
            if(len(mergeValues) >= 1):
                newAvg = sum(mergeValues) / len(mergeValues)
                vldLipidInfo.append((newLipidName, newAvg))
            
            for value in unMergeValues:
                vldLipidInfo.append((newLipidName, value))
            
            
            
    logger.info("End to process lipid info with lipid name start with DG, TG")
    vldLipidInfo = set(vldLipidInfo) #用set去除重复的部分
    vldLipidInfo = list(vldLipidInfo)#再转回list
    return vldLipidInfo        

def reduceName(lipidName):
    alpha = ' dep'
    parenthesesPart = re.search(r'(\(.*\))', lipidName).group()
    parenthesesPart = parenthesesPart[1:-1]  
    
    elems = re.split(':|/|e|d|p|\+', parenthesesPart)
    
    elems = [item for item in elems if item != '']
    
    reduceParePart = str(int(elems[0]) + int(elems[2])) + ":" + str(int(elems[1]) + int(elems[3]))
    
    flag = ''
    for i in range(1, len(alpha)):
        index = parenthesesPart.find(alpha[i])
        if(index != -1):
            flag = alpha[i]    
            break
            
    reduceParePart = reduceParePart + flag
    
    if(len(elems) == 5):
        reduceParePart = reduceParePart + "+" +  elems[-1]
        
    p1 = lipidName.find('(')
    p2 = lipidName.find(')')
    
    newLipidName = lipidName[0:p1+1] + reduceParePart + lipidName[p2:]
    
    
    #只要被调用一次，就需要保存一次新名字到原始名字的映射
    if(lipidAlias.has_key(newLipidName)):
        lipidAlias[newLipidName].add(lipidName)
    else:
        lipidAlias[newLipidName] = set([lipidName])
    
    
    
    return newLipidName


def reorderP_SM(c2TopRT):
    
    logger.info("Start to reorder the lipid-->toprts pair with the lipid name start with P and SM")
    #newc2TopRT中，key保存以DG，TG开头，括号部分经过排序的化合物，value是化合物名称经过处理后是相同的化合物的所有的topRT值
    newc2TopRT = {}
    newc2TopRTAvg = {}
    for (k,v)in c2TopRT.iteritems():
        prefix = k[0:k.find('(')]
        if(prefix[0] != "P" and prefix != "SM"):            
            continue;
        
        topRTs = c2TopRT[k]
        newLipidName = reduceName(k)
        
        if(newc2TopRT.has_key(newLipidName)):
            for topRT in topRTs:
                newc2TopRT[newLipidName].append(topRT)
        else:   
                newc2TopRT[newLipidName] = topRTs
        
    
    for (k,v) in newc2TopRT.iteritems():
        if(len(v) == 0):
            newc2TopRTAvg[k] = 0.0
        else:
            newc2TopRTAvg[k] = sum(v)/len(v)
            
    
    logger.info("End to reorder the lipid-->toprts pair with the lipid name start with P and SM")
    return (newc2TopRTAvg, newc2TopRT)    


def p2dot3(f2c, c2TopRT):
    
    logger.info("Start to process lipid info with lipid name start with DG, TG")
    vldLipidInfo = []
    (newc2TopAvg, newc2TopRT) = reorderP_SM(c2TopRT)
    for(k,v) in f2c.iteritems():
        lipidNames = list(v)
        
        for n in lipidNames:
            prefix = n[0:n.find('(')]
            #只处理DG或者TG开头的
            if(prefix[0] != "P" and prefix != "SM"):
                print("continue: prefix = " + prefix)
                continue
            
            print("prefix = " + prefix)
            newLipidName = reduceName(n)
            
            topRTs = newc2TopRT[newLipidName]
            lipidAvg = newc2TopAvg[newLipidName]
            
            print("newlipidName: " + newLipidName)
            print("topRTs: " + str(topRTs))
            print("lipidAvg: " + str(lipidAvg))
            
            #保存需要重新计算平均值的topRT值
            mergeValues = []
            #保存需要单独保存的topRT值
            unMergeValues = []
            for topRT in topRTs:
                diff = math.fabs(topRT - lipidAvg)
                
                if(diff <= topRTRange):
                    mergeValues.append(topRT)
                else:
                    unMergeValues.append(topRT)
            
            if(len(mergeValues) >= 1):
                newAvg = sum(mergeValues) / len(mergeValues)
                vldLipidInfo.append((newLipidName, newAvg))
            
            for value in unMergeValues:
                vldLipidInfo.append((newLipidName, value))
            
            
            
    logger.info("End to process lipid info with lipid name start with P, SM")
    vldLipidInfo = set(vldLipidInfo) #用set去除重复的部分
    vldLipidInfo = list(vldLipidInfo)#再转回list
    return vldLipidInfo   


def rmLipidNameIn2dot123(f2c,c2TopRTAvg,c2TopRT, c2Grade):
    
    for(k,v) in f2c.iteritems():
        lipidNames = list(v)
        nv = []
        for n in lipidNames:
            if(n[0] != "P" and getGroupNum(n) != 1 and n[0:n.find('(')] != "SM" and n[0:n.find('(')] != "DG" and n[0:n.find('(')] != "TG"):
                nv.append(n)
        
        f2c[k] = nv
        
    lipidNames = c2TopRT.keys()    
    for n in lipidNames:
        if(n[0] == "P" or getGroupNum(n) == 1 or n[0:n.find('(')] == "SM" or n[0:n.find('(')] == "DG" or n[0:n.find('(')] == "TG"):
            c2TopRT.pop(n)
            
    lipidNames = c2TopRTAvg.keys()    
    for n in lipidNames:
        if(n[0] == "P" or getGroupNum(n) == 1 or n[0:n.find('(')] == "SM" or n[0:n.find('(')] == "DG" or n[0:n.find('(')] == "TG"):
            c2TopRTAvg.pop(n)
                                                 

    lipidNames = c2Grade.keys()    
    for n in lipidNames:
        if(n[0] == "P" or getGroupNum(n) == 1 or n[0:n.find('(')] == "SM" or n[0:n.find('(')] == "DG" or n[0:n.find('(')] == "TG"):
            c2Grade.pop(n)

def getGradeMap(lipidInfo):
    
    c2Grade = {}
    
    for item in lipidInfo:
        lipidName = item[0]
        grade = item[5]
        
        if(c2Grade.has_key(lipidName)):
            c2Grade[lipidName].append(grade)
        else:
            c2Grade[lipidName] = [grade]
            

    
    return c2Grade

def isAllAB(grades):
    flag = True
    
    for g in grades:
        if(g != 'A' and g != 'B'):
            flag = False
            break
    
    return flag

def isAllCD(grades):
    flag = True
    
    for g in grades:
        if(g != 'C' and g != 'D'):
            flag = False
            break
    
    return flag

def isAllABCD(grades):
    flagAB = False
    flagCD = False
    
    for g in grades:
        if(g == 'A' or g == 'B'):
            flagAB = True;
            break
    
    for g in grades:
        if(g == 'C' or g == 'D'):
            flagCD = True;
            break
        
    if(flagAB and flagCD):
        return True
    else:
        return False
    
        

def p2dot4a(f2c, c2TopRTAvg, c2TopRT, c2Grade):
    
    logger.info("Start to process lipid with grade values as A or B")
    vldLipidInfo = []
    for(k, v) in f2c.iteritems():
        lipidNames = list(v)
        
        for n in lipidNames:
            grades = c2Grade[n]
            flag = isAllAB(grades)
            
            if(flag == False):
                continue
            
            topRTs = c2TopRT[n]
            lipidAvg = c2TopRTAvg[n]
            
            #保存需要重新计算平均值的topRT值
            mergeValues = []
            #保存需要单独保存的topRT值
            unMergeValues = []
            for topRT in topRTs:
                diff = math.fabs(topRT - lipidAvg)
                
                if(diff <= topRTRange):
                    mergeValues.append(topRT)
                else:
                    unMergeValues.append(topRT)
            
            if(len(mergeValues) >= 1):
                newAvg = sum(mergeValues) / len(mergeValues)
                vldLipidInfo.append((n, newAvg))
            
            for value in unMergeValues:
                vldLipidInfo.append((n, value))
                
                
    
    logger.info("End to process lipid with grade values as A or B")
    
    return vldLipidInfo

def reorderAllGradeCD(c2TopRT):
    newc2TopRTAvg = {}
    newc2TopRT = {}
    
    for (n, v) in c2TopRT.iteritems():
        grades = c2Grade[n]
        flag = isAllCD(grades)
       
        if(flag == False):
            continue 
        newLipidName = reduceName(n)
        
        if(newc2TopRT.has_key(newLipidName)):
            for item in v:
                newc2TopRT[newLipidName].append(item)
        else:
            newc2TopRT[newLipidName] = v
            
    
    for (n, v) in newc2TopRT.iteritems():
        if(len(v) == 0):
            newc2TopRTAvg[n] = 0.0
        else:
            newc2TopRTAvg[n] = sum(v) / len(v)
            
    
    return (newc2TopRTAvg, newc2TopRT)


            
    
    

def p2dot4b(f2c, c2TopRTAvg, c2TopRT, c2Grade):
    logger.info("Start to process lipid with grade values as C or D")
    vldLipidInfo = []
    
    (newc2TopRTAvg, newc2TopRT) = reorderAllGradeCD(c2TopRT)
    
    #print("newc2TopRT = " + str(newc2TopRT))
    
    for (k, v) in f2c.iteritems():
        lipidNames = list(v)
        
        for n in lipidNames:
            grades = c2Grade[n]
            flag = isAllCD(grades)
            
            if(flag == False):
                continue
            
            newLipidName = reduceName(n)
            
            #保存需要重新计算平均值的topRT值
            mergeValues = []
            #保存需要单独保存的topRT值
            unMergeValues = []
            
            topRTs = newc2TopRT[newLipidName]
            lipidAvg = newc2TopRTAvg[newLipidName]
            
            for topRT in topRTs:
                diff = math.fabs(topRT - lipidAvg)
                
                if(diff <= topRTRange):
                    mergeValues.append(topRT)
                else:
                    unMergeValues.append(topRT)
            
            if(len(mergeValues) >= 1):
                newAvg = sum(mergeValues) / len(mergeValues)
                vldLipidInfo.append((newLipidName, newAvg))
            
            for value in unMergeValues:
                vldLipidInfo.append((newLipidName, value))
            
            
            
    logger.info("End to process lipid with grade values as C or D")
    vldLipidInfo = set(vldLipidInfo) #用set去除重复的部分
    vldLipidInfo = list(vldLipidInfo)#再转回list
  
    return vldLipidInfo               


def reorderAllGradeABCD(c2TopRT):
    newc2TopRTAvg = {}
    newc2TopRT = {}
    
    #保存名字经过合并前的原名
    alias = {}
    
    for (n, v) in c2TopRT.iteritems():
        grades = c2Grade[n]
        flag = isAllABCD(grades)
        print("flag = " +  str(flag) + ", name = " + n + ", grades " + str(grades))
        if(flag == False):
            continue 
        newLipidName = reduceName(n)
        
        #newLipidName = n + "/" + newLipidName
        
        if(newc2TopRT.has_key(newLipidName)):
            for item in v:
                newc2TopRT[newLipidName].append(item)
        else:
            newc2TopRT[newLipidName] = v
        
        if(alias.has_key(newLipidName)):
            alias[newLipidName].add(n)
        else:
            alias[newLipidName] = set([n])
            
    
    for (n, v) in newc2TopRT.iteritems():
        if(len(v) == 0):
            newc2TopRTAvg[n] = 0.0
        else:
            newc2TopRTAvg[n] = sum(v) / len(v)
            
    
    return (newc2TopRTAvg, newc2TopRT, alias)

def genFullName(newLipidName, aliasNames):
    aliasList = sorted(list(aliasNames))
            
#     partFullName = ""
#     for n in aliasList:
#         partFullName = n + "/" + partFullName
        
    
    partFullName = aliasList[0] + "/"    
    newFullName = partFullName + newLipidName 
    
    #只要被调用一次，就需要保存一次新名字到原始名字的映射
    if(lipidAlias.has_key(newFullName)):
        lipidAlias[newFullName].add(aliasList[0])
    else:
        lipidAlias[newFullName] = set([aliasList[0]])
    
    return newFullName


def p2dot4c(f2c, c2TopRTAvg, c2TopRT, c2Grade):
    logger.info("Start to process lipid with grade values as A,B,C,D")
    vldLipidInfo = []
    
    (newc2TopRTAvg, newc2TopRT, alias) = reorderAllGradeABCD(c2TopRT)
    
    print("alias = " + str(alias))
    
    for (k, v) in f2c.iteritems():
        lipidNames = list(v)
        
        for n in lipidNames:
            grades = c2Grade[n]
            flag = isAllABCD(grades)
            
            if(flag == False):
                continue
            
            newLipidName = reduceName(n)
            
            
            #保存需要重新计算平均值的topRT值
            mergeValues = []
            #保存需要单独保存的topRT值
            unMergeValues = []
            
            topRTs = newc2TopRT[newLipidName]
            lipidAvg = newc2TopRTAvg[newLipidName]
            
            for topRT in topRTs:
                diff = math.fabs(topRT - lipidAvg)
                
                if(diff <= topRTRange):
                    mergeValues.append(topRT)
                else:
                    unMergeValues.append(topRT)
            #把合并前后的名字都组合起来
            newFullName = genFullName(newLipidName, alias[newLipidName])
            if(len(mergeValues) >= 1):
                newAvg = sum(mergeValues) / len(mergeValues)
                vldLipidInfo.append((newFullName, newAvg))
            
            for value in unMergeValues:
                vldLipidInfo.append((newFullName, value))
            
            
            
    logger.info("End to process lipid with grade values as A,B,C,D")
    vldLipidInfo = set(vldLipidInfo) #用set去除重复的部分
    vldLipidInfo = list(vldLipidInfo)#再转回list
  
    return vldLipidInfo      

def combineLipidInfo(lipidInfoIn2dot1, lipidInfoIn2dot2, lipidInfoIn2dot3, lipidInfoIn2dot4a, lipidInfoIn2dot4b, lipidInfoIn2dot4c, c2f, c2om):
    finalLipidInfo = []
    
    print("keys of c2f:" + str(list(c2f)))
    print("keys of lipidAlias:" + str(list(lipidAlias)))
    
    allPairs = lipidInfoIn2dot1 + lipidInfoIn2dot2 + lipidInfoIn2dot3 + lipidInfoIn2dot4a + lipidInfoIn2dot4b + lipidInfoIn2dot4c
    
    for item in allPairs:
        lipidName = item[0]
        topRTAvg = item[1]
        
        origLipidName = item[0]
        if(lipidAlias.has_key(lipidName)):
            origLipidName = list(lipidAlias[lipidName])[0]
        
        
        
        formula = c2f[origLipidName]
        obsMz = c2om[origLipidName]
        
        lipidFinalItem = (lipidName, formula, obsMz, topRTAvg)
        finalLipidInfo.append(lipidFinalItem)
        
    
    return finalLipidInfo
        
        
        
        
    
    return finalLipidInfo

def getAreaMap(lipidInfo):
    logger.info("Start to get lipid name mapping to area info")
    
    c2AreaList = []  
    for item in lipidInfo:
        area = item[7]
        lipidName = item[0]
        fileName = item[-1]
       
        c2AreaList.append((lipidName, fileName, area))
        for item2 in lipidInfo:
            lipidName2 = item2[0]
            if(lipidName != lipidName2):
                continue
             
            fileName2 = item[-1]
            area2 = item[7]
             
            if(fileName != fileName2):
                c2AreaList.append((lipidName, fileName2, area2))
            
            if(fileName == fileName2 and area != area2):
                c2AreaList.append((lipidName, fileName2, area2))
            
            
            
#         areaInfo = {}
#          
#         #currKey = (lipidName, fileName)
#         currKey = fileName
#         if(areaInfo.has_key(currKey)):
#             #areaInfo[currKey].append((fileName, area))
#             areaInfo[currKey].append(area)
#         else:
#             #areaInfo[currKey] = [(fileName, area)]
#             areaInfo[currKey] = [area]
#              
#         c2Area[lipidName] = areaInfo
    
    #convert c2AreaList to c2AreaMap
    
    c2AreaMap = {}
    for item in c2AreaList:
        lipidName = item[0]
        fileName = item[1]
        area = item[2]
        
        key = (lipidName, fileName)
        
        if(c2AreaMap.has_key(key)):
            c2AreaMap[key].append(area)
        else:
            c2AreaMap[key] = [area]
               
    
    logger.info("End to get lipid name mapping to area info")
    return c2AreaMap
    

    
def p6(lipidInfo):
    
    c2Area = getAreaMap(lipidInfo)
    
    logger.info("c2Area = " + str(c2Area))
    
    vldLipidAreaInfo = {}
    for item in lipidInfo:        
        lipidName = item[0]
        fileName = item[-1]  
        
        
        key = (lipidName, fileName)
            
        areas = c2Area[key]
        vldLipidAreaInfo[key] =  areas
        
#         if(vldLipidInfo.has_key(lipidName)):
#             vldLipidInfo[lipidName] = vldLipidInfo[lipidName] + areas
#         else:
#             vldLipidInfo[lipidName] =  areas   
        

                
    
    
    logger.info("p6 result = " + str(vldLipidAreaInfo))
    
    return vldLipidAreaInfo

def combineAreaInfo(finalLipidInfo, vldLipidAreaInfo, dataBook):
    
    fileNames = list(dataBook)
    
    finalAreaInfo = {}
    
    for item in finalLipidInfo:
        lipidName = item[0]
        
    
        #先处理没有别名的部分
        for f in fileNames:
            key = (lipidName, f)
            if(vldLipidAreaInfo.has_key(key)):
                finalAreaInfo[key] = vldLipidAreaInfo[key]
            
        
        #处理有别名部分
        lipidNames = []
        if(lipidAlias.has_key(lipidName)):
            lipidNames = lipidAlias[lipidName]
        
        for n in lipidNames:
            for f in fileNames:
                key1 = (lipidName, f)
                key2 = (n, f)
                
                if(finalAreaInfo.has_key(key1)):
                    finalAreaInfo[key1] = finalAreaInfo[key1] + vldLipidAreaInfo[key2]
                else:
                    if(vldLipidAreaInfo.has_key(key2)):
                        finalAreaInfo[key1] = vldLipidAreaInfo[key2]
                
        
        
        
                
                
                 
            
    for(k, v) in finalAreaInfo.iteritems():
            finalAreaInfo[k] = set(v)   
        
    logger.info("final area info = " + str(finalAreaInfo))    
    
    return finalAreaInfo
                
            
            
        
    
    
                
                
                
            
        
         
        
        

    
if __name__ == '__main__':
        
    #得到目录./lipddata下的所有文件的内容，以dict的形式组织，该dict的key是文件名，value是文件的内容，文件的内容又
    #以dict的形式进行组织，key是对应文件中的每1列的标题，value是该列对应的内容
    #dataBook = loadAllTextFile("./lipiddata", logger)
    dataBook = makeTestData()
    lipidInfo = makeTuple(dataBook)
    logger.info("Before removing item that the gap between RT and TopRT is bigger than ms2Window(0.2)")
    pprint.pprint(lipidInfo)
    logger.info("After removing item that the gap between RT and TopRT is bigger than ms2Window(0.2)")
    lipidInfo = rm0dot2(lipidInfo)
    
    (c2TopRTAvg, c2TopRT) = calTopRTAvg(lipidInfo)
    
    (f2c,c2f) = getFormulaMap(lipidInfo)
    logger.info("lipid name with same formula: " + str(f2c))
    logger.info("lipid name to formula mapping: " + str(c2f))
    
    c2Grade = getGradeMap(lipidInfo)
    logger.info("c2Grade = " + str(c2Grade))
    
    lipidInfoIn2dot1 = p2dot1(f2c, c2TopRTAvg,c2TopRT)
    logger.info("lipidInfoIn2dot1: " + str(lipidInfoIn2dot1))
    
    lipidInfoIn2dot2 = p2dot2(f2c, c2TopRT)
    logger.info("lipidInfoIn2dot2: " + str(lipidInfoIn2dot2))
    
    lipidInfoIn2dot3 = p2dot3(f2c, c2TopRT)
    logger.info("lipidInfoIn2dot3: " + str(lipidInfoIn2dot3))

    rmLipidNameIn2dot123(f2c, c2TopRTAvg, c2TopRT, c2Grade)
    logger.info("After removing lipid in step2.1,2.2,2.3, f2c = " + str(f2c))
    logger.info("After removing lipid in step2.1,2.2,2.3, c2TopRTAvg = " + str(c2TopRTAvg))
    logger.info("After removing lipid in step2.1,2.2,2.3, c2TopRT = " + str(c2TopRT))
    logger.info("After removing lipid in step2.1,2.2,2.3, c2Grade = " + str(c2Grade))
    
    lipidInfoIn2dot4a = p2dot4a(f2c, c2TopRTAvg, c2TopRT, c2Grade)
    logger.info("lipidInfoIn2dot4a: " + str(lipidInfoIn2dot4a))
    
    lipidInfoIn2dot4b = p2dot4b(f2c, c2TopRTAvg, c2TopRT, c2Grade)
    logger.info("lipidInfoIn2dot4b: " + str(lipidInfoIn2dot4b))
    
    lipidInfoIn2dot4c = p2dot4c(f2c, c2TopRTAvg, c2TopRT, c2Grade)
    logger.info("lipidInfoIn2dot4c: " + str(lipidInfoIn2dot4c))
    
    
    c2om = getObsMZMap(lipidInfo)
    #将上面所有lipidInfo[num]dot[num]的化合物归并到一起，list中的每个元素是一个元组(lipidName, formula, ObsMZ, TopRT ...)
    finalLipidInfo = combineLipidInfo(lipidInfoIn2dot1, lipidInfoIn2dot2, lipidInfoIn2dot3, lipidInfoIn2dot4a, lipidInfoIn2dot4b, lipidInfoIn2dot4c, c2f, c2om)
    
    pprint.pprint(finalLipidInfo)
    
    c2Areas = p6(lipidInfo)
    
    p6FinalResult = combineAreaInfo(finalLipidInfo, c2Areas, dataBook)
    
    ls = set()
    for item in finalLipidInfo:
        ls.add(item[0])
        
    logger.info("size1 = " + str(len(ls)))
    
    size2 = len(list(p6FinalResult))
    
    ls4 = list(p6FinalResult)
    
    ls5 = set()
    for item in ls4:
        ls5.add(item[0])
    
    size2 = len(ls5)
        
    logger.info("size2 = " + str(size2))
    
    ls2 = sorted(list(ls))
    
    ls3 = sorted(ls5)
    
    logger.info("ls2 = " + str(ls2))
    logger.info("ls3 = " + str(ls3))
    
    
    
    
    
    
    

    
    
    pass