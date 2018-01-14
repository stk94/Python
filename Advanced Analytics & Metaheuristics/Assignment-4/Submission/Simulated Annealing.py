# Question6 Simulated Annealing
# Required Libraries
from random import Random  # need this for the random number generation -- do not chan
import numpy as np
import math

# to setup a random number generator, we will specify a "seed" value
# need this for the random number generation -- do not change
seed = 5113
myPRNG = Random(seed)

# number of elements in a solution
n = 100

# create an "instance" for the knapsack problem
value = []
for i in range(0, n):
    value.append(myPRNG.uniform(10, 100)) # value of each object lies between 10 and 100

weights = []
for i in range(0, n):
    weights.append(myPRNG.uniform(5, 20)) # weight of each object lies between 5 and 20

# define max weight for the knapsack
maxWeight = 5 * n

# change anything you like below this line ------------------------------------

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
        return [-1, -1]  # print ("Oh no! The solution is infeasible!  What to do?  What to do?")   #you will probably want to change this...

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

def getCurrentTemperature(temperature_maximum, n):
    temperature_maximum = temperature_maximum /(1 + n)    # Cauchy cooling schedule
    #temperature_maximum = temperature_maximum-(n*2) #linear cooling schedule
    return temperature_maximum, n * 40

# create the initial solution
x_curr = []

def initial_solution():
    for i in range(0, n):
        if myPRNG.random() < 0.8: # if random number generated between 0 & 1 is < 0.9 then item is not selected.
            x_curr.append(0)
        else:
            x_curr.append(1)
    return x_curr

# varaible to record the number of solutions evaluated
solutionsChecked = 0
x_best = initial_solution()
f_best = f_curr = evaluate(x_curr)[0]

Solution = []
maximumtemperature = 3800  # initial temperature
maximum_Iterations = 300  # Stopping criteria

for k in range(1, maximum_Iterations):
    solutionsChecked += 1
    temperature, u = getCurrentTemperature(maximumtemperature, k)  # get a current temperature

    iterations = 0  # count iterations
    while iterations < u:  # iterate until max iteration
        s = myPRNG.choice(neighborhood(x_curr))  # selection criteria  values from the neighborhood

        if evaluate(s)[0] > f_best:  # if an improvement was found
            x_curr = x_best = s[:]  # set the curreent and best solution
            f_curr = f_best = evaluate(s)[0]  # set the current and best value
            Solution = evaluate(s)
        else:
            delta = evaluate(x_curr)[0] - evaluate(s)[0]  # difference in objective values
            prob = myPRNG.random()  # set prob to a random number

            if prob < math.exp(-1 * delta / temperature):  # if prob is less than the prob function
                x_curr = s[:]  # make the move--this is completely random
                f_curr = evaluate(s)[0]  # makes the value move

        iterations = iterations + 1

print("number of solutions checked: ", solutionsChecked)
print("Final Temperature", temperature)
print("Best value found", f_best)
print("Best weight and Value", Solution)
print("Items selected", np.sum(x_best))
print("Simulated Annealing solution: ", x_best)