
import operator
from __builtin__ import sorted

data = dict()

data["abc"] = 1
data["tef"] = 9
data["smth"] = 9

data["org"] = 6

print data

dataList = sorted(data.iteritems(),key=operator.itemgetter(1,0),reverse=True)

print dataList

if __name__ == '__main__':
    pass