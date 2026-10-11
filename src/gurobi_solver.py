import gurobipy as gp
from gurobipy import GRB
from src.sat_solver import load_sudoku
from math import sqrt
from time import perf_counter


def solve_sudoku_gurobi(file_name):
    A = load_sudoku(file_name)
    N = len(A)

    start = perf_counter()

    env = gp.Env(empty=True)
    env.setParam("LogToConsole", 0)
    env.start()

    model = gp.Model("Sudoku", env=env)
    model.setParam("OutputFlag", 0)

    x = model.addVars(
        N, N, N,
        vtype=GRB.BINARY,
        name="x"
    )


    for i in range(N):
        for j in range(N):
            if A[i][j] > 0:
                model.addConstr(x[i, j, A[i][j] - 1] == 1)


    for i in range(N):
        for j in range(N):
            model.addConstr(sum([x[i, j, k] for k in range(N)]) == 1)


    for i in range(N):
        for k in range(N):
            model.addConstr(sum([x[i, j, k] for j in range(N)]) == 1)


    for j in range(N):
        for k in range(N):
            model.addConstr(sum([x[i, j, k] for i in range(N)]) == 1)


    size_sub_matrix = int(sqrt(N))

    for i in range(0, N, size_sub_matrix):
        for j in range(0, N, size_sub_matrix):
            for k in range(N):
                model.addConstr(
                    sum([
                        x[row, col, k] 
                        for row in range(i, i + size_sub_matrix)
                        for col in range(j, j + size_sub_matrix)
                    ])
                == 1)

    end = perf_counter()
    encoding_time = round((end - start) * 1000)
    
    start = perf_counter()
    model.optimize()
    end = perf_counter()
    solve_time = round((end - start) * 1000)

    if model.Status == GRB.OPTIMAL:
        for i in range(N):
            for j in range(N):
                for k in range(N):
                    if x[i, j, k].X > 0.5:
                        A[i][j] = k + 1
                        break

    return {
        "size": N,
        "type": "Gurobi",
        "encoding_time": encoding_time,
        "solve_time": solve_time,
        "total_time": encoding_time + solve_time,
        "is_solved": model.Status == GRB.OPTIMAL
    }

if __name__ == "__main__":
    s1 = 'sudoku_puzzles/64x64/sudoku_64x64_sample_01.txt'
    s2 = 'puzzles/25x25/clue_70/sudoku_01.txt'
    print(solve_sudoku_gurobi(s2))