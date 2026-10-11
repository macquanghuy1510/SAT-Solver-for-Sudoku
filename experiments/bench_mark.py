import csv
import glob
from pathlib import Path
from pysat.card import EncType

from src.cplexcp_solver import solve_sudoku_cplexcp
from src.cplexmip_solver import solve_sudoku_cplexmip
from src.cpsat_solver import solve_sudoku_cpsat
from src.gurobi_solver import solve_sudoku_gurobi
from src.sat_solver import solve_sudoku_sat

PUZZLES = {25: sorted(glob.glob("puzzles/25x25/**/*.txt", recursive=True), reverse=True)}

SOLVERS = {
    "SAT": solve_sudoku_sat,
    "Gurobi": solve_sudoku_gurobi,
    "CPLEX_MIP": solve_sudoku_cplexmip,
    "CPLEX_CP": solve_sudoku_cplexcp,
    "CP_SAT": solve_sudoku_cpsat,
}


def benchmark_solvers():
  output_dir = Path("benchmark_data")
  output_dir.mkdir(exist_ok=True)
  csv_path = output_dir / "benchmark_solver.csv"

  headers = [
      "size",
      "clue_ratio",
      "sample",
      "solver",
      "construction_time",
      "solve_time",
      "total_time",
      "status",
      "error",
  ]

  with open(csv_path, "w", newline="", encoding="utf-8-sig") as f:
    writer = csv.writer(f)
    writer.writerow(headers)

    for size, puzzles in PUZZLES.items():
      for puzzle_path in puzzles:
        p = Path(puzzle_path)
        clue_ratio, sample = p.parent.name, p.stem

        for solver_name, solver_func in SOLVERS.items():
          row_data = [size, clue_ratio, sample, solver_name, "", "", "", "", ""]

          try:
            res = solver_func(str(p))
            row_data[4:8] = [
                res.get("encoding_time", ""),
                res.get("solve_time", ""),
                res.get("total_time", ""),
                "SUCCESS" if res.get("is_solved") else "FAILED",
            ]
            print(
                f"{size}x{size} | {clue_ratio} | {sample} | {solver_name} |"
                f" {res.get('total_time', 'N/A')} ms"
            )
          except Exception as e:
            row_data[7:9] = ["ERROR", str(e)]
            print(
                f"{size}x{size} | {clue_ratio} | {sample} | {solver_name} |"
                f" ERROR: {e}"
            )

          writer.writerow(row_data)
          f.flush()

        print("-" * 20)


ENCODINGS = {
    "Pairwise": EncType.pairwise,
    "Bitwise": EncType.bitwise,
    "SeqCounter": EncType.seqcounter,
}


def benchmark_encodings():
    output_dir = Path("benchmark_data")
    output_dir.mkdir(exist_ok=True)
    csv_path = output_dir / "benchmark_encoding.csv"

    headers = [
        "size",
        "clue_ratio",
        "sample",
        "encoding_method",
        "variables",      
        "clauses",    
        "encoding_time",
        "solve_time",
        "total_time",
        "status",
        "error",
    ]

    with open(csv_path, "w", newline="", encoding="utf-8-sig") as f:
        writer = csv.writer(f)
        writer.writerow(headers)

        puzzle_files = glob.glob("puzzles/**/clue_70/**/*.txt", recursive=True)
        valid_puzzles = []

        for puzzle_path in puzzle_files:
            p = Path(puzzle_path)
            try:
                size = int(p.parts[1].split("x")[0])
            except (IndexError, ValueError):
                continue

            if 9 <= size <= 64:
                valid_puzzles.append((size, p))

        valid_puzzles.sort(key=lambda x: x[0])

        for size, p in valid_puzzles:
            clue_ratio = p.parent.name
            sample = p.stem

            for enc_name, enc_value in ENCODINGS.items():
                row_data = [size, clue_ratio, sample, enc_name, "", "", "", "", "", "", ""]

                try:
                    res = solve_sudoku_sat(str(p), encoding_type=enc_value)
                    
                    row_data[4] = res.get("variables", "")
                    row_data[5] = res.get("clauses", "")
                    row_data[6:10] = [
                        res.get("encoding_time", ""),
                        res.get("solve_time", ""),
                        res.get("total_time", ""),
                        "SUCCESS" if res.get("is_solved") else "FAILED",
                    ]
                    row_data[10] = "" 
                    
                    print(
                        f"[ENC] {size}x{size} | {clue_ratio} | {sample} | {enc_name} | "
                        f"Vars: {row_data[4]} | Clauses: {row_data[5]} | Total: {res.get('total_time', 'N/A')} ms"
                    )
                except BaseException as e:
                    error_msg = str(e) if str(e) else type(e).__name__
                    
                    row_data[4:9] = ["", "", "", "", ""] 
                    row_data[9] = "ERROR"
                    row_data[10] = error_msg
                    
                    print(
                        f"[ENC] {size}x{size} | {clue_ratio} | {sample} | {enc_name} | "
                        f"ERROR: {error_msg}"
                    )

                writer.writerow(row_data)
                f.flush()

            print("-" * 30)


if __name__ == "__main__":
    benchmark_solvers()
    # benchmark_encodings()