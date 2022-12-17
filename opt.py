from gurobipy import *

SF = 15 # amount of fuel (gallons) in tank at origin o
MG = 30  # The average fuel economy of an average SUV in MPG
TC = 30 # vehicle tank capacity (e.g., 200 gallons)
LF = TC / 4  # minimum fuel to maintain in tank at all times (1/4 of full tank capacity)
MP = 3 # minimum amount of fuel to purchase at gas stations
EF = LF # required amount of fuel in tank at the final destination d (ending fuel)


def refuel_opt(nearest, Mile, path):
    Fuel = {0: SF}
    n = len(nearest)
    Mile_d = Mile[n - 1]
    price=[]; Out=[]
    for i in path[1:-1]:
        price.append(float(nearest[i]['Price']))
        Out.append(nearest[i]['Distance'])
    model = Model("refuel_station")
    phi, delta = {}, {}
    for i in range(n):
        phi[i] = model.addVar(vtype=GRB.INTEGER, name='p.{0}'.format(i))    #Integer amounts, why not!
    for i in range(n):
        delta[i] = model.addVar(vtype=GRB.BINARY,name='d.{0}'.format(i))
    model.update()
    for i in range(1, n-1):
        Fuel[i] = Fuel[i - 1] + phi[i - 1] - (delta[i - 1] * Out[i - 1] + Mile[i] + delta[i] * Out[i]) / MG
    Fuel[n-1] = Fuel[n - 2] + phi[n - 2] - (delta[n - 2] * Out[n - 2] + Mile[n - 1]) / MG
    for i in range(n):
        model.addConstr(Fuel[i] >= LF)
    model.addConstr(Fuel[n-1] >= EF)
    model.update()
    for i in range(n):
        model.addConstr(phi[i] >= delta[i] * MP)
        model.addConstr(phi[i] <= delta[i] * TC)
        model.addConstr(Fuel[i] + phi[i] <= TC)
    obj = quicksum(price[i] * phi[i] for i in range(n))
    model.setObjective(obj)
    model.update()
    model.optimize()
    opt_cost = model.getObjective().getValue()
    print(opt_cost)
    model.write('test.lp')
    fill_quantities=[]
    for i in range(n):
        fill_quantities.append(phi[i].X)
    return opt_cost, fill_quantities

