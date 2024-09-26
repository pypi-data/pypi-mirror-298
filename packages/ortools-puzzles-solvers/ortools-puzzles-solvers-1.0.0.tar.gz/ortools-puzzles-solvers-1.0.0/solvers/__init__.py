from ortools.sat.python import cp_model

model = cp_model.CpModel()

S = model.NewIntVar(1, 9, "S")
E = model.NewIntVar(0, 9, "E")
N = model.NewIntVar(0, 9, "N")
D = model.NewIntVar(0, 9, "D")
M = model.NewIntVar(1, 9, "M")
O = model.NewIntVar(0, 9, "O")
R = model.NewIntVar(0, 9, "R")
Y = model.NewIntVar(0, 9, "Y")

model.AddAllDifferent([S,E,N,D,M,O,R,Y])

SEND = S * 1000 + E * 100 + N * 10 + D * 1
MORE = M * 1000 + O * 100 + R * 10 + E * 1
MONEY = M * 10000 + O * 1000 + N * 100 + E * 10 + Y * 1

model.Add(SEND + MORE == MONEY)

solver = cp_model.CpSolver()
status = solver.Solve(model)
print(solver.Value(S))
print(solver.Value(E))
print(solver.Value(N))
print(solver.Value(D))

print(solver.Value(M))
print(solver.Value(O))
print(solver.Value(R))
print(solver.Value(E))

print(solver.Value(M))
print(solver.Value(O))
print(solver.Value(N))
print(solver.Value(E))
print(solver.Value(Y))