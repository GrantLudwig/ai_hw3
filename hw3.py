#hw3.py v1.0
#Grant Ludwig
#5/3/19

#Arg order:
    #1: number of iterations
    #2: number of chromosomes generated
    #3: file with the knapsack size and items
#File format:
    #First line must be knapsack size
        #must be positive integer
    #All lines after are sizes of items
        #must be positive integers

import sys
import random
import math

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

def printChromo(chromo):
    output = ''
    for gene in chromo:
        if gene:
            output += '1'
        else:
            output += '0'
    print(output)

def generateChromosomes(length):
    chromo = []
    for _ in range(length):
        chromo.append(bool(random.getrandbits(1)))
    return chromo

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

def runEvolution(chromos, iList, size, numPar):
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
    #Found solution
    if 0 in fitness:
        return (chromos[fitness.index(min(fitness))], True)
    #Probability choice
    for i in range(len(fitness)):
        fitness[i] = 1/fitness[i]
        #build tuples
    parentWeightList = []
    for i in range(len(chromos)):
        parentWeightList.append((chromos[i],fitness[i]))
    pairs = []
    floorNumPar = math.floor(numPar/2) #needed incase numPar is odd
    #Get pairs
    for _ in range(floorNumPar):
        p1 = None
        p2 = None
        while p1 == None:
            p1 = probChoice(parentWeightList)
        while p2 == None:
            p2 = probChoice(parentWeightList)
        pairs.append((p1, p2))
    #Cross/create children
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
    #Get extra chromosome if still need more
        #This will happen when the parents amount is odd
    while floorNumPar < math.ceil(numPar/2):
        children.append(generateChromosomes(len(iList)))
        floorNumPar += 1
    return (children, False)

def geneticAlg(iList, size, runs, numP):
    parents = []
    for _ in range(numP):
        parents.append(generateChromosomes(len(iList)))
    for i in range(runs):
        print('\nIteration: ', i+1)
        print('Chromosomes:')
        for parent in parents:
            printChromo(parent)
        parents, complete = runEvolution(parents, iList, size, numP)
        if complete:
            return parents
    index = fitness(size, parents, iList)
    return parents[index]
    

#Driver code
numRuns = int(sys.argv[1])
numParents = int(sys.argv[2])
fileName = sys.argv[3]
itemList, sackSize = readFile(fileName)
list = geneticAlg(itemList, sackSize, numRuns, numParents)
print('\nFinal Chromosome:')
printChromo(list)
print('\nBag size:', sackSize)
output = ''
sum = 0
for i in range(len(list)):
    if list[i]:
        output += str(itemList[i]) + ' '
        sum += itemList[i]
if sum == sackSize:
    print('Found solution:', output)
else:
    print('Found close solution:', output)