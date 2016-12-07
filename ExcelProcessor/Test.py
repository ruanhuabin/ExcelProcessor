
import operator
from __builtin__ import sorted
from util import printDict

data = dict()

data["abc"] = 1
data["tef"] = 9
data["smth"] = 9

data["org"] = 6

print data

dataList = sorted(data.iteritems(),key=operator.itemgetter(1,0),reverse=True)

print "datalist= " + str(dataList)


table = {}

table["c1"] = [[1,2,3]]
table["c2"] = [[4,5,6]]
table["c5 c4 (%)"] = []

table.get("c5 c4 (%)").append([7,8,9])

c5c4data = table["c5 c4 (%)"]
print "c5c4data = ", c5c4data

print table


a = [1,2,3,4,5,23]

average = float(sum(a)) / len(a)
print average

table2 = {}
table2["c1"] = [{"key1":1}, {"key1":2}]
print table2


def getKey(item):
    return item[0]
data = [["c5", 1], ["c3", 2], ["c4", 8]]

data.sort(cmp=None, key=getKey, reverse=True)
print data

a = 3
b = "Hello B"
str1 = "This is a message: [%s:%d]" % (b, a)


print str1




def addValueToDict(key, table, item):
    origValues = table[key]
    origValues.append(item)
    
    table[key] = origValues
    
    return table

def reverseDictTest(dictData):
    
    newDict = {}
    for(k,v) in dictData.iteritems():
        v = str(v[0])
        if(newDict.has_key(v)):
            newDict[v].append(k)
        else:
            newDict[v] = [k]
            
    return newDict
  
import re 
def getGroupNum(compndName):
    
    parenthesesPart = re.search('\(.*\)', compndName).group();   
    print("parenthesesPart = " + str(parenthesesPart))
    semicolon = re.findall(':', str(parenthesesPart))  
    
    print("semicolon = " + str(semicolon))    
    
    return len(semicolon)

def getGroupNum2(compndName):
    
    parenthesesPart = re.search(r'((.*))', compndName).group();   
    print("parenthesesPart = " + str(parenthesesPart))
    semicolon = re.findall(':', str(parenthesesPart))  
    
    print("semicolon = " + str(semicolon))    
    
    return len(semicolon)
            

def reduceName(lipidName):
    alpha = ' dep'
    parenthesesPart = re.search(r'(\(.*\))', lipidName).group()
    parenthesesPart = parenthesesPart[1:-1] 
    
    print("parenthesesPart = " + parenthesesPart)
    
    elems = re.split(':|/|e|d|p|\+', parenthesesPart)
    
    
    
    print("elems = " + str(elems))
    
    elems = [item for item in elems if item != '']
    print("after remove, elems = " + str(elems))
    
    reduceParePart = str(int(elems[0]) + int(elems[2])) + ":" + str(int(elems[1]) + int(elems[3]))
    print("reduceParePart = " + reduceParePart)
    
    flag = ''
    for i in range(1, len(alpha)):
        index = parenthesesPart.find(alpha[i])
        print("index = " + str(index))
        if(index != -1):
            flag = alpha[i]
            print("flag = "+ flag)
            break
            
    reduceParePart = reduceParePart + flag
    print("new reduceParePart = " + reduceParePart)
    
    if(len(elems) == 5):
        reduceParePart = reduceParePart + "+" +  elems[-1]
        
    print("final reduceParePart = " + reduceParePart)
        
    p1 = lipidName.find('(')
    p2 = lipidName.find(')')
    
    newLipidName = lipidName[0:p1+1] + reduceParePart + lipidName[p2:]
    
    print("final lipid name = " + newLipidName)
    

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

if __name__ == '__main__':
    
    
    grades = ['C', 'A', 'C']
    
    flag = isAllCD(grades)

    print("flag =" + str(flag))
    
    
    l1 = [1,2,3]
    l2 = [4,5,6]
    l3 = [(7,8),9]
    
    l4 = l1 + l2 + l3 
    
    print(l4)
    
    l5 = []
    l5.append([x for x in l1])
    print l5
    
#     num =  getGroupNum('TG(9:0/9:0/19:4)+NH4')
#     print("num = " + str(num))
    
#     dictData3 = {}
#     dictData3["a"] = ["va"]
#     dictData3["b"] = ["va"]
#     dictData3["c"] = ["vc"]
#     
#     newDict3 = reverseDictTest(dictData3)
#     print newDict3
    
#     pass
# 
#     
#     key = "key1"
#     myTable = {}
#     myTable[key] = ["item1", "item2"]
#     
#     print myTable
#     addValueToDict(key, myTable, "item3")
#     print myTable
#     
#     
#     li = ['A', 'C', 'B', 'D']
#     
#     if('A' in li):
#         print "True"
#     
#     if('F' in li):
#         print "True"
#     else:
#         print "False"
#         
#         
#     
#     mySet = set()
#     li2 = [[1,2], [3,4],[5,6]]
#     #li2 = str(li2)
#     for item in li2:
#         mySet.add(str(item))
#         
#     print mySet
#     pass