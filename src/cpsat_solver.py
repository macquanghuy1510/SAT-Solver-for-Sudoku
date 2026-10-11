from ortools.sat.python import cp_model
from src.sat_solver import load_sudoku
from math import sqrt
from time import perf_counter


def solve_sudoku_cpsat(file_name):

    A = load_sudoku(file_name)
    N = len(A)

    model = cp_model.CpModel()

    start = perf_counter()


    x = [
        [
            model.NewIntVar(1, N, f"x_{i}_{j}")
            for j in range(N)
        ]
        for i in range(N)
    ]


    for i in range(N):
        for j in range(N):
            if A[i][j] > 0:
                model.Add(x[i][j] == A[i][j])


    for i in range(N):
        model.AddAllDifferent(x[i])


    for j in range(N):
        model.AddAllDifferent(
            [x[i][j] for i in range(N)]
        )


    size_sub_matrix = int(sqrt(N))

    for i in range(0, N, size_sub_matrix):
        for j in range(0, N, size_sub_matrix):

            cells = [
                x[row][col]
                for row in range(i, i + size_sub_matrix)
                for col in range(j, j + size_sub_matrix)
            ]

            model.AddAllDifferent(cells)

    end = perf_counter()

    encoding_time = round((end - start) * 1000)

    solver = cp_model.CpSolver()

    solver.parameters.log_search_progress = False

    start = perf_counter()

    status = solver.Solve(model)

    end = perf_counter()

    solve_time = round((end - start) * 1000)

    result = status in (
        cp_model.OPTIMAL,
        cp_model.FEASIBLE
    )

    if result:
        for i in range(N):
            for j in range(N):
                A[i][j] = solver.Value(x[i][j])

    return {
        "size": N,
        "type": "CP-SAT",
        "encoding_time": encoding_time,
        "solve_time": solve_time,
        "total_time": encoding_time + solve_time,
        "is_solved": result
    }


if __name__ == "__main__":
    s1 = 'sudoku_puzzles/64x64/sudoku_64x64_sample_01.txt'
    s2 = 'puzzles/25x25/clue_70/sudoku_01.txt'
    print(solve_sudoku_cpsat(s2))