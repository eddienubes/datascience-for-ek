from ortools.linear_solver import pywraplp
import matplotlib.pyplot as plt
import numpy as np

solver = pywraplp.Solver.CreateSolver('GLOP')

x1 = solver.NumVar(0, solver.infinity(), 'X1')
x2 = solver.NumVar(0, solver.infinity(), 'X2')
x3 = solver.NumVar(0, solver.infinity(), 'X3')
x4 = solver.NumVar(0, solver.infinity(), 'X4')
x5 = solver.NumVar(0, solver.infinity(), 'X5')
x6 = solver.NumVar(0, solver.infinity(), 'X6')

print("Number of variables =", solver.NumVariables())

solver.Add(1.5 * x1 + 2 * x2 <= 12 + x4.solution_value())
solver.Add(x1 + 2 * x2 <= 8 + x3.solution_value())
solver.Add(4 * x1 <= 16 + x5.solution_value())
solver.Add(4 * x2 <= 12 + x6.solution_value())

print("Number of constraints =", solver.NumConstraints())

solver.Minimize(-2 * x1 - 2 * x2)

status = solver.Solve()

if status == pywraplp.Solver.OPTIMAL:
    x1 = x1.solution_value()
    x2 = x2.solution_value()
    x3 = x1 + 2 * x2 - 8
    x4 = 1.5 * x1 + 2 * x2 - 12
    x5 = 4 * x1 - 16
    x6 = 4 * x2 - 12

    print('Solution:')
    print('X1 =', x1)
    print('X2 =', x2)
    print('X3 =', x3)
    print('X4 =', x4)
    print('X5 =', x5)
    print('X6 =', x6)

    print('Optimal objective value (Q) =', solver.Objective().Value())

    x = np.linspace(0, 10, 400)
    y1 = (12 - 1.5 * x) / 2
    y2 = (8 - x) / 2
    y3 = np.full_like(x, 4)  # 4*X1 <= 16 -> X1 <= 4
    y4 = 3  # 4*X2 <= 12 -> X2 <= 3

    plt.figure(figsize=(10, 8))

    plt.plot(x, y1, label=r'$1.5X1 + 2X2 \leq 12$')
    plt.plot(x, y2, label=r'$X1 + 2X2 \leq 8$')
    plt.axvline(x=4, label=r'$X1 \leq 4$', color='green')
    plt.axhline(y=3, label=r'$X2 \leq 3$', color='purple')

    # Fill the feasible region
    plt.fill_between(x, np.minimum.reduce([y1, y2, np.full_like(x, 3)]), 0, where=(x <= 4), color='grey', alpha=0.5)

    plt.plot(x1, x2, 'ro', label='Optimal Solution')

    plt.xlim((0, 5))
    plt.ylim((0, 5))
    plt.xlabel(r'$X1$')
    plt.ylabel(r'$X2$')
    plt.title('Feasible Region and Optimal Solution')
    plt.legend()
    plt.grid(True)
    plt.show()
else:
    print('There is no solution')
