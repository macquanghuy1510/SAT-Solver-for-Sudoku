from pysat.card import *
from math import sqrt
from pysat.solvers import Solver
from time import perf_counter


def load_sudoku(file_name):
    with open(file_name, "r") as f:
        A = [list(map(int, line.split())) for line in f]

    return A


def varmap(i, j, k, N):
    return i * N**2 + j * N + k


def solve_sudoku_sat(file_name, encoding_type = 1, solver_name = 'g3'):
    A = load_sudoku(file_name)
    N = len(A)

    start = perf_counter()
    cnf = CNF()
    vpool = IDPool(start_from = N**3 + 1)


    def encode_eo(arr):
        eo = CardEnc.equals(
            lits = arr,
            encoding = encoding_type,
            vpool = vpool
        )
        cnf.extend(eo)

    for i in range(N):
        for j in range(N):
            if A[i][j] != 0:
                cnf.append([varmap(i, j, A[i][j], N)])


    for i in range(N):
        for j in range(N):
            encode_eo([varmap(i, j, k, N) for k in range(1, N + 1)])


    for i in range(N):
        for k in range(1, N + 1):
            encode_eo([varmap(i, j, k, N) for j in range(N)])


    for j in range(N):
        for k in range(1, N + 1):
            encode_eo([varmap(i, j, k, N) for i in range(N)])


    size_sub_matrix = int(sqrt(N))

    for i in range(0, N, size_sub_matrix):
        for j in range(0, N, size_sub_matrix):
            for k in range(1, N + 1):
                encode_eo([
                    varmap(row, col, k, N)
                    for row in range(i, i + size_sub_matrix)
                    for col in range(j, j + size_sub_matrix)
                ])

    end = perf_counter()
    encoding_time = round((end - start) * 1000)

    solver = Solver(name = solver_name)
    solver.append_formula(cnf)
    start = perf_counter()
    result = solver.solve()
    end = perf_counter()
    solve_time = round((end - start) * 1000)


    if result:
        model = solver.get_model()
        var_true = [var for var in model if var > 0 and var <= N**3]
        idx = 0
        for i in range(N):
            for j in range(N):
                A[i][j] = var_true[idx] - (i * N**2 + j * N)
                idx += 1
    else:
        print("UNSAT")

    return {
        "size": N,
        "solver": solver_name,
        "type": "SAT Solving",
        "variables": cnf.nv,
        "clauses": len(cnf.clauses),
        "encoding_time": encoding_time,
        "solve_time": solve_time,
        "total_time": encoding_time + solve_time,
        "is_solved": result
    }


if __name__ == "__main__":
    s1 = 'sudoku_puzzles/64x64/sudoku_64x64_sample_01.txt'
    s2 = 'puzzles/25x25/clue_70/sudoku_01.txt'
    print(solve_sudoku_sat(s2, EncType.seqcounter))