#hw3.py v1.0
#Grant Ludwig
#5/3/19

import sys
import random

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
            iList.append(int(line))
    return (iList, bagSize)

def generateChromosomes(length):
    chromo = []
    for _ in range(length):
        chromo.append(bool(random.getrandbits(1)))
    return chromo

def geneticAlg(iList, size):
    parents = []
    fitness = []
    for _ in range(10):
        parents.append(generateChromosomes(len(iList)))
    #Fitness
    for parent in parents:
        sum = 0
        for i in range(len(parent)):
            if parent[i]:
                sum += iList[i]
        fitness.append(sum)
    print(fitness)
    for i in range(len(fitness)):
        fitness[i] = abs(size - fitness[i])
    print(fitness)
    #Choose best
    parentIList = []
    for _ in range(6):
        index = fitness.index(min(f for f in fitness if f > 0))
        parentIList.append(index)
        fitness[index] = -1
    print(parentIList)
    #Cross
    

#Driver code
fileName = sys.argv[1]
itemList, sackSize = readFile(fileName)
geneticAlg(itemList, sackSize)