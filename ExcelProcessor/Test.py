
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
print "data.sort = " + str(data)

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
    
    
    
    t4 = {}
    t4["123"] = [1,2,3]
    v = t4["123"]
    print("v = " + str(v))
    
    
    smallerValues = [12.377, 12.347, 12.325, 12.288, 12.342, 12.364, 12.36, 12.27, 12.349, 12.314, 12.35, 12.326, 12.305, 12.389, 12.326, 12.383, 12.279, 12.211, 12.364, 12.32, 12.331, 12.347, 12.338, 12.327, 12.296, 12.292, 12.299, 12.299, 12.262, 12.316, 12.291, 12.261, 12.348, 12.349, 12.342, 12.3, 12.302, 12.24, 12.264, 12.332, 12.334, 12.309, 12.271, 12.189, 12.362, 12.377, 12.347, 12.236, 12.291, 10.684, 12.291, 12.353, 10.685, 12.24, 10.653, 10.702, 12.384, 10.663, 12.325, 12.317, 12.288, 10.724, 12.282, 12.312, 10.666, 12.297, 12.372, 10.679, 10.659, 10.664, 10.663, 10.708, 10.659, 10.7, 10.646, 10.645, 10.713, 10.703, 10.634, 10.689, 12.28, 10.666, 10.681, 10.672, 10.692, 10.695, 10.655, 12.346, 10.669, 10.665, 10.711, 10.694, 12.26, 12.3, 12.258, 10.703, 10.686, 12.327, 10.662, 10.647, 10.677, 10.714, 10.717, 10.655, 10.67, 10.689, 10.717, 12.272, 12.298, 12.287, 12.307, 10.681, 10.669, 10.693, 12.287, 10.656, 10.634, 10.672, 10.709, 10.631, 12.271, 10.634, 10.671, 10.677, 12.33, 10.709, 10.689, 12.349, 10.701, 10.655, 12.28, 10.663, 12.337, 10.649, 10.647, 10.644, 10.669, 10.681, 12.288, 10.707, 10.657, 10.651, 12.251, 12.386, 10.696, 10.677, 10.693, 12.35, 10.714, 12.303, 10.661, 10.727, 12.281, 10.645, 12.223, 10.706, 10.69, 10.673, 10.702, 12.368, 10.673, 10.653, 12.316, 10.685, 10.647, 10.648, 10.662, 12.344, 10.654, 10.704, 10.653, 10.645, 12.278, 10.652, 12.383, 12.316, 10.701, 10.692, 10.657, 10.701, 10.708, 12.308, 12.262, 10.645, 10.693, 10.647, 10.667, 10.623, 10.642, 10.728, 12.364, 10.723, 10.7, 10.639, 12.32, 10.649, 10.68, 10.688, 10.671, 10.67, 12.268, 12.31, 10.686, 12.365, 10.666, 10.701, 10.635, 12.322, 10.696, 10.694, 10.68, 12.347, 10.689, 10.669, 10.648, 10.697, 10.691, 10.657, 10.662, 10.666, 10.075, 10.701, 12.296, 10.669, 10.692, 10.691, 10.654, 10.643, 10.693, 10.653, 10.679, 10.642, 10.683, 10.697, 10.683, 10.675, 12.346, 10.694, 10.687, 10.711, 10.681, 12.288, 12.279, 10.667, 10.69, 12.284, 10.689, 12.262, 12.33, 10.684, 12.326, 10.68, 10.694, 10.695, 10.695, 10.697, 10.685, 10.631, 10.661, 10.682, 10.682, 12.291, 10.66, 12.33, 10.702, 10.674, 10.657, 10.64, 10.656, 10.711, 10.67, 10.664, 10.69, 12.342, 10.682, 10.694, 10.678, 10.703, 10.678, 10.659, 10.69, 12.348, 10.694, 10.619, 10.669, 10.697, 12.31, 10.681, 10.679, 12.334, 12.274, 10.698, 12.29, 10.692, 10.65, 12.352, 10.652, 10.661, 10.659, 10.701, 10.722, 10.677, 10.662, 12.241, 10.674, 12.312, 10.709, 10.65, 10.668, 10.669, 10.691, 10.728, 12.322, 10.704, 12.327, 10.66, 10.683, 12.278, 10.697, 10.671, 12.371, 10.71, 12.363, 10.677, 10.73, 12.314, 10.694, 12.209, 10.661, 10.643, 12.276, 10.642, 12.342, 10.691, 10.662, 12.332, 10.653, 10.643, 10.685, 10.65, 10.668, 10.646, 12.334, 10.68, 12.364, 10.686, 10.701, 12.334, 10.666, 10.647, 10.677, 10.671, 12.284, 12.358, 12.358, 10.711, 10.689, 12.377, 10.654, 10.674, 10.699, 10.667, 12.307, 10.688, 12.34, 10.672, 10.682, 10.683, 10.685, 12.333, 10.673, 10.643, 10.656, 12.31, 10.699, 10.682, 10.699, 10.69, 10.644, 12.349, 12.271, 12.308, 10.719, 10.67, 12.381, 10.657, 10.687, 10.661, 10.709, 12.24, 10.678, 10.677, 12.298, 12.329, 10.69, 10.699, 10.679, 10.673, 12.347, 12.315, 10.675, 10.66, 10.667, 10.68, 10.653, 10.646, 10.701, 10.647, 10.682, 12.336, 10.699, 10.652, 10.66, 10.692, 12.32, 12.282, 10.655, 10.647, 10.647, 10.737, 12.328, 10.715, 10.667, 10.666, 10.693, 12.322, 12.234, 12.385, 12.325, 12.339, 12.282, 12.297, 12.372, 12.342, 12.292, 12.281, 12.265, 12.228, 12.282, 12.33, 12.282, 12.321, 12.28, 12.312, 12.322, 12.298, 12.346, 12.295, 12.319, 12.316, 12.327, 12.335, 12.324, 12.285, 12.265, 12.36, 12.272, 12.287, 12.295, 12.383, 12.349, 12.254, 12.355, 12.327, 12.27, 12.271, 12.337, 12.322, 12.375, 12.349, 12.327, 12.337, 12.306, 12.284, 12.314, 12.361, 12.355, 12.241, 12.313, 12.347, 12.35, 12.361, 12.326, 12.278, 12.343, 12.293, 12.274, 12.316, 12.305, 12.344, 12.309, 12.278, 12.326, 12.316, 12.299, 12.25, 12.308, 12.262, 12.211, 12.298, 12.283, 12.364, 12.31, 12.356, 12.32, 12.246, 12.32, 12.341, 12.261, 12.365, 12.302, 12.331, 12.305, 12.267, 12.296, 12.347, 12.247, 12.351, 12.338, 12.327, 12.385, 12.305, 12.263, 12.385, 12.335, 12.296, 12.303, 12.328, 12.293, 12.237, 12.306, 12.309, 12.273, 12.299, 12.261, 12.346, 12.321, 12.288, 12.275, 12.357, 12.262, 12.33, 12.335, 12.314, 12.245, 12.298, 12.344, 12.286, 12.277, 12.283, 12.34, 12.253, 12.342, 12.339, 12.301, 12.287, 12.338, 12.348, 12.224, 12.31, 12.366, 12.342, 12.334, 12.274, 12.364, 12.29, 12.349, 12.352, 12.306, 12.261, 12.341, 12.293, 12.343, 12.322, 12.36, 12.327, 12.283, 12.278, 12.289, 12.352, 12.363, 12.317, 12.39, 12.365, 12.209, 12.254, 12.28, 12.276, 12.286, 12.342, 12.365, 12.249, 12.307, 12.302, 12.364, 12.289, 12.353, 12.324, 12.334, 12.299, 12.241, 12.358, 12.342, 12.307, 12.332, 12.34, 12.365, 12.273, 12.334, 12.28, 12.31, 12.309, 12.349, 12.308, 12.359, 12.381, 12.346, 12.316, 12.24, 12.333, 12.329, 12.311, 12.284, 12.377, 12.347, 12.315, 12.322, 12.274, 12.309, 12.291, 12.336, 12.298, 12.32, 12.282, 12.197, 12.301, 12.328, 12.267, 10.678, 12.386, 10.696, 12.349, 10.22]
    avg = sum(smallerValues) / len(smallerValues)
    print("avg = " + str(avg))
    
    smallerValues.sort()
    print("smallerValues = " + str(smallerValues))
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