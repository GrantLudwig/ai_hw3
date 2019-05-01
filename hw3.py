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

#TODO Better
def probChoice(choices):
    selectionSpace = {}
    current = 0
    for choice, weight in choices:
        if weight > 0:
            selectionSpace[current] = choice
            current += weight
    rand = random.uniform(0, current)
    for key in sorted(selectionSpace.keys()):
        if rand < key:
            return choice
        choice = selectionSpace[key]
    return None

def fitness(size, chromos, iList):
    fitness = []
    #Fitness
    for parent in chromos:
        sum = 0
        for i in range(len(parent)):
            if parent[i]:
                sum += iList[i]
        fitness.append(sum)
    for i in range(len(fitness)):
        fitness[i] = abs(size - fitness[i])
    return fitness.index(min(fitness))

def runEvolution(chromos, iList, size):
    fitness = []
    #Fitness
    for parent in chromos:
        sum = 0
        for i in range(len(parent)):
            if parent[i]:
                sum += iList[i]
        fitness.append(sum)
    for i in range(len(fitness)):
        fitness[i] = abs(size - fitness[i])
    #TODO correct return
    if 0 in fitness:
        return (chromos[fitness.index(min(fitness))], True)
    #Probability choice
    #TODO better prob
    for i in range(len(fitness)):
        fitness[i] = 1/fitness[i]
    #build tuples
    parentWeightList = []
    for i in range(len(chromos)):
        parentWeightList.append((chromos[i],fitness[i]))
    pairs = []
    #num pairs = 3
    for _ in range(3):
        p1 = None
        p2 = None
        while p1 == None:
            p1 = probChoice(parentWeightList)
        while p2 == None:
            p2 = probChoice(parentWeightList)
        pairs.append((p1, p2))
    #Cross
    children = []
    for p1, p2 in pairs:
        child1 = []
        child2 = []
        randIndex = random.randrange(1, len(p1)-1)
        for i in range(0,randIndex):
            child1.append(p1[i])
            child2.append(p2[i])
        for i in range(randIndex, len(p1)):
            child1.append(p2[i])
            child2.append(p1[i])
        children.append(child1)
        children.append(child2)
    #mutation
    for child in children:
        if bool(random.getrandbits(1)):
            randIndex = random.randrange(0, len(child))
            child[randIndex] = not child[randIndex]
    return (children, False)

def generateChromosomes(length):
    chromo = []
    for _ in range(length):
        chromo.append(bool(random.getrandbits(1)))
    return chromo

def geneticAlg(iList, size):
    parents = []
    #6 parents
    for _ in range(6):
        parents.append(generateChromosomes(len(iList)))
    for i in range(40):
        print('\n Run: ', i+1)
        parents, complete = runEvolution(parents, iList, size)
        if complete:
            return parents
    index = fitness(size, parents, iList)
    return parents[index]
    

#Driver code
fileName = sys.argv[1]
itemList, sackSize = readFile(fileName)
list = geneticAlg(itemList, sackSize)
output = ''
for i in range(len(list)):
    if list[i]:
        output += str(itemList[i]) + ' '
print('\n')
print(output)