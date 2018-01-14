#Question 7: Variable Neighborhood Search
# Required Libraries

from random import Random   #need this for the random number generation -- do not change
import numpy as np
from random import randrange, uniform

#to setup a random number generator, we will specify a "seed" value
#need this for the random number generation -- do not change
seed = 5113
myPRNG = Random(seed)

#number of elements in a solution
n = 100

#create an "instance" for the knapsack problem
value = []
for i in range(0,n):
    value.append(myPRNG.uniform(10,100)) # value of each object lies between 10 and 100

weights = []
for i in range(0,n):
    weights.append(myPRNG.uniform(5,20))  # weight of each object lies between 5 and 20

#define max weight for the knapsack
maxWeight = 5*n

#monitor the number of solutions evaluated
solutionsChecked = 0

#function to evaluate a solution x
def evaluate(x):
    a=np.array(x)
    b=np.array(value)
    c=np.array(weights)

    totalValue = np.dot(a,b)     #compute the value of the knapsack selection
    totalWeight = np.dot(a,c)    #compute the weight value of the knapsack selection

    if totalWeight > maxWeight:  #If the solution is infeasible we simply ignore it
        return [-1, -1]

    return [totalValue, totalWeight]   #returns a list of both total value and total weight

#  Create the initial solution
x_curr = []
def initial_solution():
    for i in range(0, n):
        if myPRNG.random() < 0.8: # item will not be selected if random number generated is less than 0.8
            x_curr.append(0)
        else:
            x_curr.append(1)
    return x_curr

def Variable_Neighbor(x, k): # k refers to number of flips
    neighboorhood = []
    no_flips = []
    for i in range(0,n):
        neighboorhood.append(x[:])
        no_flips = [myPRNG.randint(0, n - 1) for u in range(0, k)]
        for j in no_flips:
            if neighboorhood[i][j] == 1:
                neighboorhood[i][j] = 0
            else:
                neighboorhood[i][j] = 1
    return neighboorhood

solutionsChecked = 0

x_best = initial_solution()  #x_curr will hold the current solution
f_curr = evaluate(x_curr)   #f_curr will hold the evaluation of the current soluton
f_best = f_curr[:]
k = 0
k_max = 3

#begin local search overall logic ----------------
done = 0
while k < k_max:
    k = k + 1
    while done == 0:
        #Neighborhood = neighborhood(x_curr)
        Neighborhood = Variable_Neighbor(x_curr, k)
        k = k + 1
        for s in Neighborhood:                #evaluate every member in the neighborhood of x_curr
            solutionsChecked = solutionsChecked + 1
            if evaluate(s)[0] > f_best[0]:
                x_best = s[:]                 #find the best member and keep track of that solution
                f_best = evaluate(s)[:]       #and store its evaluation

        if f_best == f_curr:               #if there were no improving solutions in the neighborhood
            done = 1
        else:
            x_curr = x_best[:]         #else: move to the neighbor solution and continue
            f_curr = f_best[:]         #evalute the current solution

            print ("\nTotal number of solutions checked: ", solutionsChecked)
            print ("Best value found so far: ", f_best)

print ("\nFinal number of solutions checked: ", solutionsChecked)
print ("Best value found: ", f_best[0])
print ("Weight is: ", f_best[1])
print ("Total number of items selected: ", np.sum(x_best))
print ("Best solution: ", x_best)
