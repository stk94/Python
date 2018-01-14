# Guided Local Search

# need some python libraries
import copy
import math
import numpy as np
import operator
import scipy.spatial.distance
from random import Random

# to setup a random number generator, we will specify a "seed" value
from sklearn.metrics.classification import fbeta_score
seed = 12345
myPRNG = Random(seed)

# to get a random number between 0 and 1, write call this:             myPRNG.random()
# to get a random number between lwrBnd and upprBnd, write call this:  myPRNG.uniform(lwrBnd,upprBnd)
# to get a random integer between lwrBnd and upprBnd, write call this: myPRNG.randint(lwrBnd,upprBnd)

posMax = 500 # maximum value for solution
posMin = -500 # minimum value for solution

# Name: evaluate()
# Parameter: x(solution)
# Return: val(value of evaluation)
# Schwefel function to evaluate a real-valued solution x
# note: the feasible space is an n-dimensional hypercube centered at the origin with side length = 2 * 500
def evaluate(x):
    val = 0
    d = len(x)
    for i in range(d):
        val = val + x[i] * math.sin(math.sqrt(abs(x[i])))
    val = 418.9829 * d - val
    return val

# Name: neighborhood()
# Parameter: dim(dimension, from 2 to 200); x(initial solution); N(neighborhood size);
#            lower(lowerbound value to generate random value to add/substract to the value of initial solution);
#            upper(upperbound value to generate random value to add/substract to the value of initial solution)
# Return: neighbors
# Create neighborhood for initial solution
def neighborhood(dim, x, N, lower, upper):
    neighbors = []
    prob = 0.3 # probability to decide whether add/substract
    for i in range(N):
        neighbor = []
        for j in range(dim):
            if prob < myPRNG.random():
                # add random value
                pos = x[j] + myPRNG.uniform(lower,upper)
            else:
                # substract initial solution with random value
                pos = x[j] - myPRNG.uniform(lower,upper)
            # set the solution to boundary if infeasible
            if pos < posMin:
                posVal = posMin
            elif pos > posMax:
                posVal = posMax
            else:
                posVal = pos
            neighbor.append(posVal)
        neighbors.append(neighbor[:])
    return neighbors

# Name: initialSolution()
# Parameter: dim(dimension)
# Return: x(initial solution)
def initialSolution(dim):
    x = []
    for i in range(dim):
        x.append(myPRNG.uniform(posMin, posMax))
    return x

# Name: features()
# Parameter: x;s (solution)
# Return: feature (indicator result for each feature for a solution)
# feature for gls
# 1. distance from the local optimum < 10
# 2. the solution contain value 0
def features(x, s):
    nFeatures = 2 #number of features
    # euclidian distance
    eD = scipy.spatial.distance.euclidean(x, s)
    # calculate indicator result for feature 1
    if eD < 10 : f1 = 1
    else: f1 = 0
    # calculate indicator result for feature 2
    if 0 in s: f2 = 1
    else: f2 = 0
    feature = [f1,f2]
    return feature

# Name: initialP()
# Paramater : nFeature(number of feature)
# Return: p
# Initial penalty value (0)
def initialP(nFeature):
    p = []
    for i in range(nFeature):
        p.append(0)
    return p

# Name: getLambda()
# Parameter: x(solution); f(indicator feature)
# Return: lmbda
# Calculate lambda value
def getLambda(x,f):
    alpha = 0.5
    lmbda = alpha * (evaluate(x)/len(f))
    return lmbda

# Name: evaluateGLS()
# Parameter: s(solution); f(indicator feature); p(penalty)
# Return: value (evaluation value)
# Calculate extended move evaluation value
def evaluateGLS(s,f,p):
    value = 0
    aF = np.array(f)
    aP = np.array(p)
    fp = np.multiply(aF,aP)
    value = evaluate(s) + (getLambda(s,f)*(sum(fp)))
    return value

# Name: utility()
# Parameter: x(solution); f(indicator feature); p(penalty)
# Return: util
# Calculate utility for each feature
def utility(x,f,p):
    util = f * (evaluate(x)/(1+p))
    return util

# Name: gls()
# Parameter: dim(dimension, from 2 to 200); steps(number of iteration); N(neighborhood size);
#            lower(lowerbound value to generate random value to add/substract to the value of initial solution);
#            upper(upperbound value to generate random value to add/substract to the value of initial solution)
# Guided local search
def gls(dim,steps,N,lower,upper):
    itermax = steps
    iter = 0
    nFeature = 2
    x_curr = initialSolution(dim) # initial solution
    x_best = x_curr[:]
    xBest = x_best[:]
    p = initialP(nFeature) # initial penalty for feature
    while iter < itermax:
        Neighborhood = neighborhood(dim, x_curr, N, lower, upper) # neighborhood for x_curr
        for s in Neighborhood:
            feat_best = features(x_curr, x_best) # feature for x_best
            f_best = evaluateGLS(x_best, feat_best, p) # extended move evaluation for x_best
            featS = features(x_curr,s) # feature for solution s
            f_s = evaluateGLS(s,featS,p) # extended move evaluation for solution s
            if f_s < f_best:
                x_best = s
        sStar = x_best
        if evaluateGLS(sStar,features(x_curr,sStar),p) < evaluateGLS(x_curr,features(x_curr,x_curr),p):
            x_curr = sStar
            if(evaluate(x_curr)<evaluate(xBest)):
                xBest = x_curr
        else:
            util = []
            for i in range(nFeature):
                u = utility(x_curr,features(x_curr,x_curr)[i],p[i])
                util.append(u)
            index, value = max(enumerate(util), key=operator.itemgetter(1)) # get the feature that has the maximum utility
            p[index] = p[index] + 1
            xBest = x_curr
            fBest = evaluate(xBest)
        iter = iter + 1
    return xBest, fBest

# gls result with:
# dimension : 2
# number of iteration: 500
# neighborhood size: 500
# lowerbound value to generate neighborhood: -500
# upperbound value to generate neighborhood: 500
print(gls(2,500,500,-500,500))
