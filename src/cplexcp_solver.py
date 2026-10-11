from docplex.cp.model import CpoModel
from src.sat_solver import load_sudoku
from math import sqrt
from time import perf_counter


def solve_sudoku_cplexcp(file_name):
    A = load_sudoku(file_name)
    N = len(A)

    model = CpoModel(name="Sudoku")

    start = perf_counter()

    x = [
        [
            model.integer_var(1, N, name=f"x_{i}_{j}")
            for j in range(N)
        ]
        for i in range(N)
    ]

    for i in range(N):
        for j in range(N):
            if A[i][j] > 0:
                model.add(x[i][j] == A[i][j])


    for i in range(N):
        model.add(model.all_diff(x[i]))


    for j in range(N):
        model.add(
            model.all_diff(
                [x[i][j] for i in range(N)]
            )
        )


    size_sub_matrix = int(sqrt(N))

    for i in range(0, N, size_sub_matrix):
        for j in range(0, N, size_sub_matrix):
            cells = [
                x[row][col]
                for row in range(i, i + size_sub_matrix)
                for col in range(j, j + size_sub_matrix)
            ]

            model.add(model.all_diff(cells))

    end = perf_counter()

    encoding_time = round((end - start) * 1000)


    start = perf_counter()

    solution = model.solve(
        LogVerbosity="Quiet"
    )

    end = perf_counter()

    solve_time = round((end - start) * 1000)

    if solution:
        for i in range(N):
            for j in range(N):
                A[i][j] = solution[x[i][j]]

    return {
        "size": N,
        "type": "CplexCP",
        "encoding_time": encoding_time,
        "solve_time": solve_time,
        "total_time": encoding_time + solve_time,
        "is_solved": solution is not None
    }


if __name__ == "__main__":
    s1 = 'sudoku_puzzles/64x64/sudoku_64x64_sample_01.txt'
    s2 = 'puzzles/25x25/clue_40/sudoku_01.txt'
    print(solve_sudoku_cplexcp(s2))