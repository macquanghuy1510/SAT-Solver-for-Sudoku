from docplex.mp.model import Model
from src.sat_solver import load_sudoku
from math import sqrt
from time import perf_counter


def solve_sudoku_cplexmip(file_name):
    A = load_sudoku(file_name)
    N = len(A)

    start = perf_counter()
    model = Model(name="Sudoku")

    x = model.binary_var_cube(N, N, N, name="x")


    for i in range(N):
        for j in range(N):
            if A[i][j] > 0:
                model.add_constraint(x[i, j, A[i][j] - 1] == 1)


    for i in range(N):
        for j in range(N):
            model.add_constraint(sum([x[i, j, k] for k in range(N)]) == 1)


    for i in range(N):
        for k in range(N):
            model.add_constraint(sum([x[i, j, k] for j in range(N)]) == 1)


    for j in range(N):
        for k in range(N):
            model.add_constraint(sum([x[i, j, k] for i in range(N)]) == 1)


    size_sub_matrix = int(sqrt(N))

    for i in range(0, N, size_sub_matrix):
        for j in range(0, N, size_sub_matrix):
            for k in range(N):
                model.add_constraint(
                    sum([
                        x[row, col, k] 
                        for row in range(i, i + size_sub_matrix)
                        for col in range(j, j + size_sub_matrix)
                    ])
                == 1)

    end = perf_counter()
    encoding_time = round((end - start) * 1000)

    start = perf_counter()
    solution = model.solve()
    end = perf_counter()
    solve_time = round((end - start) * 1000)

    sudoku = [[0] * N for _ in range(N)]

    for i in range(N):
        for j in range(N):
            for k in range(N):
                if x[i, j, k].solution_value > 0.5:
                    sudoku[i][j] = k + 1

    return {
        "size": N,
        "type": "CplexMIP",
        "encoding_time": encoding_time,
        "solve_time": solve_time,
        "total_time": encoding_time + solve_time,
        "is_solved": solution is not None
    }


if __name__ == "__main__":
    s1 = 'sudoku_puzzles/64x64/sudoku_64x64_sample_01.txt'
    s2 = 'puzzles/25x25/clue_70/sudoku_01.txt'
    print(solve_sudoku_cplexmip(s2))