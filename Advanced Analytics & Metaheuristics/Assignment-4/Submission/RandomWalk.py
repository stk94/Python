# Local Search with Random Walk
# Required Libraries
from random import Random  # need this for the random number generation -- do not chan
import numpy as np
import math

# to setup a random number generator, we will specify a "seed" value
# need this for the random number generation -- do not change
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

# function to evaluate a solution x
def evaluate(x):
    a = np.array(x)
    b = np.array(value)
    c = np.array(weights)

    totalValue = np.dot(a, b)  # compute the value of the knapsack selection
    totalWeight = np.dot(a, c)  # compute the weight value of the knapsack selection

    if totalWeight > maxWeight:
        #print( "Oh no! The solution is infeasible!  What to do?  What to do?")  # you will probably want to change this...
        return [-1, -1]
    return [totalValue, totalWeight]  # returns a list of both total value and total weight

# here is a simple function to create a neighborhood
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
    x = []
    for i in range(100):
        if i < 10:
            x.append(1)    # First 10 elements are selected
        else:
            x.append(0)    # 11 to 100 elements are not selected
    return (x)

# varaible to record the number of solutions evaluated
solutionsChecked = 0

x_curr = initial_solution()  # x_curr will hold the current solution
x_best = x_curr[:]  # x_best will hold the best solution
f_curr = evaluate(x_curr)  # f_curr will hold the evaluation of the current soluton
f_best = f_curr[:]

# begin local search overall logic ----------------
done = 0
loc=0
prob = 0.75 # probability variable
sol = []

while done == 0:
    sol.append(f_best)
    Neighborhood = neighborhood(x_curr)  # create a list of all neighbors in the neighborhood of x_curr
    step= myPRNG.uniform(0,1) # step gets initialised to any value between 0 and 1
    if step < prob:
        for s in Neighborhood:  # evaluate every member in the neighborhood of x_curr
            solutionsChecked = solutionsChecked + 1
            if evaluate(s)[0] > f_best[0]:
                x_best = s[:]  # find the best member and keep track of that solution
                f_best = evaluate(s)[:]  # stores its evaluation
    else:
        walk = 0
        while walk == 0:
            solutionsChecked = solutionsChecked + 1
            rand_index = myPRNG.randint(0,98)
            s = Neighborhood[rand_index]
            if evaluate(s)[0] >= 0:
                x_best = s[:]  # find the best member and keep track of that solution
                f_best = evaluate(s)[:]  # stores its evaluation

                walk = 1

    if f_best == f_curr:  # if there are no improving solutions in the neighborhood
            done = 1
    else:
        x_curr = x_best[:]  # else: move to the neighbor solution and continue
        f_curr = f_best[:]  #  to evalute the current solution

        print("\nTotal number of solutions checked: ", solutionsChecked)
        print("Best value found so far: ", f_best)

    if solutionsChecked > 40000:  # Stopping criteria
        done = 1

print("Max solution is ", max(sol))
print("\nFinal number of solutions checked: ", solutionsChecked)
print("Best value found: ", f_best[0])
print("Weight is: ", f_best[1])
print("Total number of items selected: ", np.sum(x_best))
print("Random Walk with Best improvement solution is: ", x_best)