import mipx
model = mipx.CpModel()

# x = model.addVar(10, 1001, name="x")
# y = model.addVar(10, 1001, name="y")
# z = model.addVar(10, 10000, name="z")
# model.addGenConstrMultiplication(z, [y, x])

x = model.addVar(vtype=mipx.INTEGER, name="x")
y = model.addVar(vtype=mipx.INTEGER, name="y")
z = model.addVars(10, ub=300, vtype=mipx.INTEGER, name="z")
# xx = [z[i]+z[i+1] for i in range(9)]
model.addElement(x, z.quickselect(), y)  # z[x]=y
# model.addConstr(x + y <= 5)
model.setObjective(y)
status = model.optimize(mipx.MAXIMIZE)
if status == mipx.OptimizationStatus.OPTIMAL or status == mipx.OptimizationStatus.FEASIBLE:
    print(f"Optimal value: {model.ObjVal}")
    mipx.debugVar(x)
    mipx.debugVar(y)
    mipx.debugVar(z)
    # mipx.debugVar(o)
