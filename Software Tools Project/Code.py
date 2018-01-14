from pulp import *
import itertools
county = ["canadian","cleveland","grady","lincoln","logan","McClain","Oklahoma"]    # Set i(representing counties)
hospital = ["Hospital_Canadian","Hospital_Cleveland","Hospital_Grady","Hospital_Lincoln","Hospital_Logan","Hospital_McCalin","Hospital_Oklahoma"]  # set j(representing hspital in each county)
hospital_type = ['small','medium','large']  # set k(representing type of hospital)

arc_dist = [[6.4,57.6,57.2,70.7,62.4,45.9,34.4],  # represents distance between each county and hospital
            [51.7,6.8,27,46.1,48.6,24.4,24.1],
            [40.3,44.8,12.6,78.6,71.2,23.9,43.2],
            [82,62.2,80.4,20,56.9,69.1,53],
            [53.7,62.4,64.2,55.5,18,52.9,44.9],
            [60.9,19.8,18.4,65.2,57.8,21.2,33.3],
            [46.8,35.2,47.4,20.3,19.7,36.1,17.8]]
dist = makeDict([county,hospital],arc_dist)

Budget = 1000000000 #  Budget allocated to the project

print("dist=",dist)

pop_county = {"canadian":126123,"cleveland":269340,"grady":53685,"lincoln":34351,"logan":44422,"McClain":36511,"Oklahoma":755245}   #populations for each county
total_cost = {'small':75664804,'medium':290526109,'large':432541576}        #costs for small, medioum and large hospitals
print("population as per county =",pop_county,"Total cost for each type of hospital",total_cost)

prob = LpProblem("P-Median Hospital Location problem",LpMinimize)  # Minimizing maximum distance

Avars = LpVariable.dicts("Serving",(county,hospital,hospital_type),0,None,LpBinary)          #creating Binary varaibles for the existance of the hospitals
Evars = LpVariable.dicts("Existence",(hospital,hospital_type),0,None,LpBinary)         #creating binary variable which determines whether a site has a hospital of certain type
Pvars = LpVariable.dicts("population",(hospital,hospital_type),0,None,LpInteger)            # Integer variable which controls the population covered by each hospital
D = LpVariable("D",lowBound=0,upBound=None,cat = 'Continuous')                      #Continuous varaible reperesting the total distance

prob += D # OBJECTIVE FUNCTION is to minimize sum of distances between each county and its associated hospital

print("Avars=",Avars)
print("Evars=",Evars)

for i in county:
    prob += lpSum(Avars[i][j][k] for j in hospital for k in hospital_type) == 1 # subject to one hospital is allocated for each county

prob += lpSum(Avars[i][j][k]*dist[i][j] for i in county for j in hospital for k in hospital_type) <= D  # subject to total distance

prob += lpSum(Evars [j][k]* total_cost[k] for j in hospital for k in hospital_type) <= Budget  # subject to Budjet

prob += lpSum(Evars[j][k] for j in hospital for k in hospital_type) <= 5  # Maximum of 5 hospitals can be established

# These constraints prevents Existing of more than 1 type of hospital at the same location
prob += Evars['Hospital_Canadian']['small']  + Evars['Hospital_Canadian']['medium'] + Evars['Hospital_Canadian']['large'] <=1
prob += Evars['Hospital_Cleveland']['small']  + Evars['Hospital_Cleveland']['medium'] + Evars['Hospital_Cleveland']['large'] <=1
prob += Evars['Hospital_Grady']['small']  + Evars['Hospital_Grady']['medium'] + Evars['Hospital_Grady']['large'] <=1
prob += Evars['Hospital_Lincoln']['small']  + Evars['Hospital_Lincoln']['medium'] + Evars['Hospital_Lincoln']['large'] <=1
prob += Evars['Hospital_Logan']['small']  + Evars['Hospital_Logan']['medium'] + Evars['Hospital_Logan']['large'] <=1
prob += Evars['Hospital_McCalin']['small']  + Evars['Hospital_McCalin']['medium'] + Evars['Hospital_McCalin']['large'] <=1
prob += Evars['Hospital_Oklahoma']['small']  + Evars['Hospital_Oklahoma']['medium'] + Evars['Hospital_Oklahoma']['large'] <=1

# subject to no district assigned to unused hospital
for j in hospital:
    for k in hospital_type:
        prob += lpSum(Avars[i][j][k] for i in county) <= Evars[j][k]*7 # Maximum of 7 counties can be assigned to one hospital

# subject to population served by each site
for j in hospital:
    for k in hospital_type:
        prob += lpSum((Avars[i][j][k]* pop_county[i])for i in county) == Pvars[j][k]

# Based on the population, small, medium or large hospital is being build
for j in hospital:
    prob += 0<= Pvars[j]['small'] <= Evars[j]['small']*100000
    prob += Evars[j]['medium']*100000<= Pvars[j]['medium'] <= Evars[j]['medium']*500000
    prob += Evars[j]['large']*500000 <= Pvars[j]['large']

print(prob)
prob.writeLP("P-Median Hospital Allocation problem.lp")
prob.solve()
print("Status:",LpStatus[prob.status])

# To print variables that are selected
for i in prob.variables():
    if i.varValue==1:
        print("The following hospitals have been selected:",i)

print("Minimum Distance:",value(prob.objective))
print("Budget Used = ",lpSum(Evars [j][k]* total_cost[k] for j in hospital for k in hospital_type))



