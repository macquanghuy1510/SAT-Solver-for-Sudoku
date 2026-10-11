import math
import random


def make_puzzle(N, clue_ratio, seed=None):
    if math.isqrt(N) ** 2 != N:
        raise ValueError("N phải là số chính phương")
    if not 0 <= clue_ratio <= 100:
        raise ValueError("clue_ratio phải nằm trong [0, 100]")

    rnd = random.Random(seed)
    B = math.isqrt(N)

    def shuffled(seq):
        seq = list(seq)
        rnd.shuffle(seq)
        return seq

    rows = [g * B + r 
            for g in shuffled(range(B))
            for r in shuffled(range(B))
        ]
    
    cols = [g * B + c 
            for g in shuffled(range(B))
            for c in shuffled(range(B))
        ]
    
    nums = [x + 1 for x in shuffled(range(N))]

    def pattern(r, c):
        return (B * (r % B) + r // B + c) % N

    grid = [[nums[pattern(r, c)] for r in rows] for c in cols]

    total = N * N
    num_clues = round(total * clue_ratio / 100)
    cells = [(r, c) for r in range(N) for c in range(N)]

    for r, c in rnd.sample(cells, total - num_clues):
        grid[r][c] = 0

    return grid


if __name__ == "__main__":
    puzzle = make_puzzle(25, clue_ratio=0.6, seed=42)

    for row in puzzle:
        print(row)
