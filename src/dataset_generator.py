import random
import numpy as np
from pathlib import Path
from src.sudoku_generator import make_puzzle


SIZES = [9, 16, 25, 36, 49, 64]
CLUE_RATIOS = list(range(70, 5, -5))
SAMPLES = 5
OUTPUT_DIR = Path("puzzles")


def save_puzzle(grid, filepath):
    filepath.parent.mkdir(parents=True, exist_ok=True)

    with filepath.open("w", encoding="utf-8") as f:
        for row in grid:
            f.write(" ".join(map(str, row)) + "\n")


def main():
    rnd = random.Random(42)
    count = 0

    for N in SIZES:
        for ratio in CLUE_RATIOS:
            folder = OUTPUT_DIR / f"{N}x{N}" / f"clue_{int(ratio)}"

            for i in range(1, SAMPLES + 1):
                seed = rnd.randrange(10**9)
                puzzle = make_puzzle(N, ratio, seed)

                filepath = folder / f"sudoku_{i:02d}.txt"
                save_puzzle(puzzle, filepath)
                count += 1

            print(f"Đã sinh: {folder}")

    print(f"\nHoàn thành! Tổng cộng {count} Sudoku.")


if __name__ == "__main__":
    main()
