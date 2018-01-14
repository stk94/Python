#Local Search with Best Improvement
# Required Libraries

from random import Random
import numpy as np
import math

# seed is used to get same instance of the problem
seed = 5113
myPRNG = Random(seed)
n = 100 # 100 objects

value = []
for i in range(0, n):
    value.append(myPRNG.uniform(10, 100)) # value of each object lies between 10 and 100

weights = []
for i in range(0, n):
    weights.append(myPRNG.uniform(5, 20)) # weight of each object lies between 5 and 20

maxWeight = 5 * n # maximum weight limit

print ("value =", value) # values of objects
print ("weights=", weights) # weights of objects

def evaluate(x):
    a = np.array(x)
    b = np.array(value)
    c = np.array(weights)

    totalValue = np.dot(a, b)  # compute the value of the knapsack selection
    totalWeight = np.dot(a, c)  # compute the weight value of the knapsack selection

    if totalWeight > maxWeight:
        return [-1,-1]
    return [totalValue, totalWeight]  # returns a list of both total value and total weight

#1-flip neighborhood of solution x
def neighborhood(x):
    nbrhood = []

    for i in range(0, n):
        nbrhood.append(x[:])
        if nbrhood[i][i] == 1:
            nbrhood[i][i] = 0
        else:
            nbrhood[i][i] = 1
    return nbrhood

# create the initial solution
def initial_solution():
        x=[]
        for i in range(0, n):
            if i < 10:
                x.append(1)   # First 10 elements are selected
            else:
                x.append(0)   # 11 to 100 elements are not selected
        return x

#Initial = initial_solution()
#print ("Initial Solution = ", Initial)

# varaible to record the number of solutions evaluated

solutionsChecked = 0

x_curr = initial_solution()  # x_curr will hold the current solution
x_best = x_curr[:]  # x_best will hold the best solution
f_curr = evaluate(x_curr)  # f_curr will hold the evaluation of the current soluton
f_best = f_curr[:]

done = 0

while done == 0:

    Neighborhood = neighborhood(x_curr)  # create a list of all neighbors in the neighborhood of x_curr

    for s in Neighborhood:  # evaluate every member in the neighborhood of x_curr
        solutionsChecked = solutionsChecked + 1
        if evaluate(s)[0] > f_best[0] and evaluate(s)[1] <= maxWeight:
            x_best = s[:]  # find the best member and keep track of that solution
            f_best = evaluate(s)[:]  # and store its evaluation

    if f_best == f_curr:  # if there were no improving solutions in the neighborhood
        done = 1
    else:

        x_curr = x_best[:]  # else: move to the neighbor solution and continue
        f_curr = f_best[:]  # evalute the current solution

        #print("\nTotal number of solutions checked: ", solutionsChecked)
        #print("Best value found so far: ", f_best)

print("\nFinal number of solutions checked: ", solutionsChecked)
print("Best value found: ", f_best[0])
print("Weight is: ", f_best[1])
print("Total number of items selected: ", np.sum(x_best))
print("Local search with Best Improvement solution: ", x_best)

