#Local Search with Random Restarts
# need some python libraries
from random import Random  # need this for the random number generation -- do not change
import numpy as np
import random

# seed is used to get same instance of the problem
seed = 5113
myPRNG = Random(seed)
n = 100 # number of elements in a solution

# create an "instance" for the knapsack problem
value = []
for i in range(0, n):
    value.append(myPRNG.uniform(10, 100)) # value of each object lies between 10 and 100

weights = []
for i in range(0, n):
    weights.append(myPRNG.uniform(5, 20)) # weight of each object lies between 5 and 20

# define max weight for the knapsack
maxWeight = 5 * n

# monitor the number of solutions evaluated
solutionsChecked = 0
rand_best = []
initial = 0
restarts = 100

# function to evaluate a solution x
def evaluate(x):
    a = np.array(x)
    b = np.array(value)
    c = np.array(weights)

    totalValue = np.dot(a, b)  # compute the value of the knapsack selection
    totalWeight = np.dot(a, c)  # compute the weight value of the knapsack selection

    if totalWeight > maxWeight:
        return [-1,-1]
    return [totalValue, totalWeight]  # returns a list of both total value and total weight

# 1-flip neighborhood of solution x
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
    x = [0] * 100             # initial solution donot consider any of the element.
    no_restarts = 10          # variable to adjust number of restarts, here number of restarts=10

    if initial == 1:
        for i in range(0, no_restarts):
            x[i] = 1
            random.shuffle(x)
    return x

# varaible to record the number of solutions evaluated
solutionsChecked = 0


for i in range(0,restarts):
    done = 0
    x_curr = initial_solution()  # x_curr will hold the current solution
    initial = 1
    x_best = x_curr[:]  # x_best will hold the best solution
    f_curr = evaluate(x_curr)  # f_curr will hold the evaluation of the current soluton
    f_best = f_curr[:]

    while done == 0:
        Neighborhood = neighborhood(x_curr)  # creates a list of all neighbors in the neighborhood of x_curr
        for s in Neighborhood:  # evaluate every member in the neighborhood of x_curr
            solutionsChecked = solutionsChecked + 1
            if evaluate(s)[0] > f_best[0]:
                x_best = s[:]  # find the best member and keep track of that solution
                f_best = evaluate(s)[:]  # and store its evaluation

        if f_best == f_curr:  # if there were no improving solutions in the neighborhood
            rand_best.append(f_best)
            done = 1
        else:

            x_curr = x_best[:]  # else: move to the neighbor solution and continue
            f_curr = f_best[:]  # evalute the current solution

print("\nTotal number of solutions checked: ", solutionsChecked)
print("Best value found so far: ", max(rand_best))
print("Total number of items selected: ", np.sum(x_best))
print("Random Restart with Best improvement solution is : ", x_best)