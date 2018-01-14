#particle swarm optimization for Schwefel minimization problem


#need some python libraries
import copy
import math
from random import Random
import operator
import numpy as np

#to setup a random number generator, we will specify a "seed" value
seed = 12345
myPRNG = Random(seed)

#to get a random number between 0 and 1, write call this:             myPRNG.random()
#to get a random number between lwrBnd and upprBnd, write call this:  myPRNG.uniform(lwrBnd,upprBnd)
#to get a random integer between lwrBnd and upprBnd, write call this: myPRNG.randint(lwrBnd,upprBnd)


#number of dimensions of problem
n = 2

#number of particles in swarm
swarmSize = 5


#Schwefel function to evaluate a real-valued solution x    
# note: the feasible space is an n-dimensional hypercube centered at the origin with side length = 2 * 500
               
def evaluate(x):          
      val = 0
      d = len(x)
      for i in range(d):
            val = val + x[i]*math.sin(math.sqrt(abs(x[i])))
                                        
      val = 418.9829*d - val         
                    
      return val          


# weight function
def weight(num_iter):
    result = 1 / math.exp(0.005 * num_iter)
    return result

# the swarm will be represented as a list of positions, velocities, values, pbest, and pbest values

pos = [[] for _ in range(swarmSize)]      #position of particles -- will be a list of lists
vel = [[] for _ in range(swarmSize)]      #velocity of particles -- will be a list of lists

curValue = [] # value of current position  -- will be a list of real values
# local best positions
pbest = []    # particles' best historical position -- will be a list of lists
pbestVal = []  # value of pbest position  -- will be a list of real values
# global best position
gbest = []  # a simple list
gbestVal = 10000000  # a very big number

#initialize the swarm randomly
for i in range(swarmSize):
    for j in range(n):
        pos[i].append(myPRNG.uniform(-500,500))    #assign random value between -500 and 500
        vel[i].append(myPRNG.uniform(-1,1))        #assign random value between -1 and 1

num_iteration = 0
vel_max = 1
vel_min = -1
pos_max = 500
pos_min = -500
theta1 = 1.8  # for cognitive component
theta2 = 0.5  # for social component
# loop until reach the max number of iterations
while num_iteration < 1000:

    # reset current values
    curValue = []

    # evaluate current
    for i in range(swarmSize):
        curValue.append(evaluate(pos[i]))   #evaluate the current position

    if num_iteration == 0:
        pbest = pos[:]  # initialize pbest to the starting position
        pbestVal = curValue[:]  # initialize pbest to the starting position
        # gbest = pbest[0]
        # gBestval = pbestVal[0]

    # Find gbest
    if min(curValue) < gbestVal:
        gbestVal = min(curValue)
        gbest = pos[curValue.index(min(curValue))]

    # will have r1 and r2 for each particle
    r1 = myPRNG.uniform(0, 1)
    r2 = myPRNG.uniform(0, 1)
    for i in range(swarmSize):
        # === update velocity ===
        # velocity equation
        vel_array = np.array(vel[i])
        pBest_array = np.array(pbest[i])
        pos_array = np.array(pos[i])
        gBest_array = np.array(gbest)
        print("pos", pos_array)
        print("vel", vel_array)
        print("gbest", gBest_array)
        vel_array = weight(num_iteration)*vel_array \
                    + theta1*r1*np.subtract(pBest_array, pos_array) \
                    + theta2*r2*np.subtract(gBest_array, pos_array)
        # set max and min for velocity
        for j in range(n):
            if vel_array[j] > vel_max:
                vel_array[j] = vel_max
            elif vel_array[j] < vel_min:
                vel_array[j] = vel_min

        # === update position ===
        pos_array = np.add(pos_array, vel_array)

        # check that positions are still between the boundaries
        for k in range(n):
            if pos_array[k] > pos_max:
                pos_array[k] = pos_max
            if pos_array[k] < pos_min:
                pos_array[k] = pos_min

        # convert from numpy to array
        pos[i] = pos_array.tolist()
        vel[i] = vel_array.tolist()

    # increase number of iterations
    num_iteration += 1

    print("Best val so far", gbestVal)

