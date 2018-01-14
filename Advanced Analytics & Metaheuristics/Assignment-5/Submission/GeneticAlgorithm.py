#Genetic Algorithm for Schwefel minimization problem

# for DSA 5113

# need some python libraries
import copy
import math
from random import Random
import numpy as np

# to setup a random number generator, we will specify a "seed" value
seed = 5113
myPRNG = Random(seed)

dimensions = 2  # set dimensions for Schwefel Function search space
lowerBound = -500  # bounds for Schwefel Function search space
upperBound = 500  # bounds for Schwefel Function search space

# you may change anything below this line that you wish too -----------------------------------------------------------------

# Student name(s):
# Date:

populationSize = 20  # size of GA population
Generations = 100  # number of GA generations

crossOverRate = 0.8
mutationRate = 0.3


# create an continuous valued chromosome
def createChromosome(d, lBnd, uBnd):
    x = []
    for i in range(d):
        x.append(myPRNG.uniform(lBnd, uBnd))  # creating a randomly located solution
    #print("x=",x)
    return x

parents = []

popVals = []
# create initial population
def initializePopulation():  # n is size of population; d is dimensions of chromosome
    population = []
    populationFitness = []

    for i in range(populationSize):
        population.append(createChromosome(dimensions, lowerBound, upperBound))
        populationFitness.append(evaluate(population[i]))
    print(" Initial population=",population)
    #print("Population Fitness=",populationFitness)
    tempZip = zip(population, populationFitness)
    popVals = sorted(tempZip, key=lambda tempZip: tempZip[1])
    #print("Parent(popVals)",popVals)    # comment created
    # the return object is a sorted list of tuples:
    # the first element of the tuple is the chromosome; the second element is the fitness value
    # for example:  popVals[0] is represents the best individual in the population
    # popVals[0] for a 2D problem might be  ([-70.2, 426.1], 483.3)  -- chromosome is the list [-70.2, 426.1] and the fitness is 483.3
    #print("PopVals=", popVals) # refers to 10 th chromosome - 1 refers to value
    #print("PopVals[9][0]",popVals[9][0])
    return popVals

# implement a linear crossover
def crossover(x1, x2):

    d = len(x1)  # dimensions of solution

    # choose crossover point

    # we will choose the smaller of the two [0:crossOverPt] and [crossOverPt:d] to be unchanged
    # the other portion be linear combo of the parents

    crossOverPt = myPRNG.randint(1,
                                 d - 1)  # notice I choose the crossover point so that at least 1 element of parent is copied
    #print("Crossover pt",crossOverPt)

    beta = myPRNG.random()  # random number between 0 and 1

    # note: using numpy allows us to treat the lists as vectors
    # here we create the linear combination of the soltuions
    new1 = list(np.array(x1) - beta * (np.array(x1) - np.array(x2)))
    new2 = list(np.array(x2) + beta * (np.array(x1) - np.array(x2)))

    # the crossover is then performed between the original solutions "x1" and "x2" and the "new1" and "new2" solutions
    if crossOverPt < d / 2:
        offspring1 = x1[0:crossOverPt] + new1[crossOverPt:d]  # note the "+" operator concatenates lists
        offspring2 = x2[0:crossOverPt] + new2[crossOverPt:d]
    else:
        offspring1 = new1[0:crossOverPt] + x1[crossOverPt:d]
        offspring2 = new2[0:crossOverPt] + x2[crossOverPt:d]

    return offspring1, offspring2  # two offspring are returned

def SortPopulation(X):
    print("X=",X)
    print("Type of X =",type(X))
    X_sorted = []
    X_fitness = []
    print("type of X_fitness",type(X_fitness))
    for i in range(populationSize):
        print ("type of X[i]",type(X[i]))
        print("X[i]=",X[i])
        X_fitness.append(evaluate(X[i]))
        print("evaluate(X[i]",evaluate(X[i]))
        #X_fitness[i]= evaluate(X[i])
    X_zip = zip(X,X_fitness)
    X_Vals = sorted(X_zip, key=lambda X_zip: X_zip[1])
    j=0
    for j in range (dimensions):
        X_sorted.append(X_Vals[j][0])
        j = j +1

    return X_sorted


# function to evaluate the Schwefel Function for d dimensions
def evaluate(x):
    val = 0
    d = len(x)
    for i in range(d):
        val = val + x[i] * math.sin(math.sqrt(abs(x[i])))

    val = 418.9829 * d - val

    return val


# function to provide the rank order of fitness values in a list
# not currently used in the algorithm, but provided in case you want to...
def rankOrder(anyList):
    rankOrdered = [0] * len(anyList)
    for i, x in enumerate(sorted(range(len(anyList)), key=lambda y: anyList[y])):
        rankOrdered[x] = i

    return rankOrdered


# performs tournament selection; k chromosomes are selected (with repeats allowed) and the best advances to the mating pool
# function returns the mating pool with size equal to the initial population
def tournamentSelection(pop, k):
    # randomly select k chromosomes; the best joins the mating pool
    matingPool = []

    while len(matingPool) < populationSize:
        ids = [myPRNG.randint(0, populationSize - 1) for i in range(k)] # out of 3(randomly selected), 1(best) chromosome is sent to mating pool..like this it happens 20 times.
        competingIndividuals = [pop[i][1] for i in ids]
        #print("competing individuals(in tournament selection) =",competingIndividuals) # comment added
        bestID = ids[competingIndividuals.index(min(competingIndividuals))]
        #print("Best of Tournament selection is(Sent to mating pool)",pop[bestID][0])  # comment added
        matingPool.append(pop[bestID][0])

    #print("Mating pool:",matingPool)  # comment added
    return matingPool

# function to mutate solutions

def mutate(x):
    rnd = myPRNG.random() # NOTICE: i did not use the mutation rate nor mutate anything... fix this!
    mut_gene = myPRNG.randint(0,dimensions-1)
    if rnd < mutationRate:
        x[mut_gene] = myPRNG.uniform(lowerBound, upperBound)
        #print("New gene created is:",x[mut_gene])
        #print("Mutated Chromosome is:", x)
    return x

childVals = []
children_Sorted = []
def breeding(matingPool):
    # the parents will be the first two individuals, then next two, then next two and so on

    children = []
    childrenFitness = []
    for i in range(0, populationSize - 1, 2):

        prob = myPRNG.random()  # random number between 0 and 1

        if prob > crossOverRate:
            child1, child2 = matingPool[i], matingPool[i + 1]

        else:
            child1, child2 = crossover(matingPool[i], matingPool[i + 1])

        child1 = mutate(child1)
        child2 = mutate(child2)

        children.append(child1)
        children.append(child2)

        childrenFitness.append(evaluate(child1))
        childrenFitness.append(evaluate(child2))

    tempZip = zip(children, childrenFitness)
    childVals = sorted(tempZip, key=lambda tempZip: tempZip[1])
    #print("Children Population after breeding = ",childVals)  # comment added
    # the return object is a sorted list of tuples:
    # the first element of the tuple is the chromosome; the second element is the fitness value
    # for example:  popVals[0] is represents the best individual in the population
    # popVals[0] for a 2D problem might be  ([-70.2, 426.1], 483.3)  -- chromosome is the list [-70.2, 426.1] and the fitness is 483.3


    return childVals

#print("childVals[9][0]=",childVals[9][0])
# insertion step
def insert(pop, kids):
    BestPop = []
    BestPop_fitness = []
    combined = pop + kids
    #print("pop=", pop)
    #print("kids=", kids)
    #print("combined before sorting=",combined)

    combined = sorted(combined, key=lambda combined: combined[1])
    #print("combined after sorting=", combined)

    #ranked = rankOrder(combined)
    d = len(pop)
    for i in range(d):
        BestPop.append(combined[i])

    #for j in range(d):
      #  BestPop_fitness.append(BestPop[j][1])

    #print("Bestpop_Fitness",BestPop_fitness)
    print("Bestpop",BestPop)
    return BestPop

    #return kids


# perform a simple summary on the population: returns the best chromosome fitness, the average population fitness, and the variance of the population fitness
def summaryFitness(pop):
    a = np.array(list(zip(*pop))[1])
    #print(np.min(a), np.mean(a), np.var(a))
    #print("Mean fitness value of Final population:",np.mean(a))
    #print("Variance of fitness value of Final population:", np.var(a))
    #print("Best Fitness value found so far:", np.min(a))
    return np.min(a), np.mean(a), np.var(a)

# the best solution should always be the first element... if I coded everything correctly...
def bestSolutionInPopulation(pop,j):
    print("Best solution found after",j+1,"generations is:",pop[0])
    #print(pop[0])
    print("Best Fitness value after",j+1,"generations is:", pop[0][1])

# optional: you can output results to a file
f = open('out.txt', 'w')

# GA main code
Population = initializePopulation()

for j in range(Generations):
    mates = tournamentSelection(Population, 3)
    Offspring = breeding(mates)
    #Population = SortPopulation(Population)
    #Offspring = SortPopulation(Offspring)
    Population = insert(Population, Offspring)

    minVal, meanVal, varVal = summaryFitness(Population)
    f.write(str(minVal) + " " + str(meanVal) + " " + str(varVal) + "\n")
    bestSolutionInPopulation(Population,j)

    #print("Best Fitness value after",Generations,"generations is",)

f.close()

#print(summaryFitness(Population))
#print("Best solution found so far is:")
#bestSolutionInPopulation(Population,Generations-1)
#print("Fitness value of Best chromosome is",)

"""
def mutate(x):
    for i in range (dimensions):
        rnd = myPRNG.random()
        if rnd <= mutationRate:
            temp = x[i]
            print("Original value of gene before mutation",temp,"i value",i)
            x[i] = temp + 3*(myPRNG.uniform(-1,1))
            print("New gene created is:", x[i])
            print("Mutated Chromosome is:", x)

    return x
"""