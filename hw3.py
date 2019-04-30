#hw3.py v1.0
#Grant Ludwig
#5/3/19

import sys

def readFile(fileName):
    firstLine = True
    bagSize = 0
    iList = []
    for line in open(fileName):
        line = line.rstrip()
        if firstLine:
            bagSize = int(line)
            firstLine = False
        else:
            iList.append(index(line))
    return (iList, bagSize)

#Driver code
fileName = sys.argv[1]
itemList, sackSize = readFile(fileName)
