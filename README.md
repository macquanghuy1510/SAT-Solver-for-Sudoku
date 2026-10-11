# SAT Solver for Sudoku

This project investigates SAT encodings for Sudoku solving and compares their performance with other optimization and constraint programming solvers.

## Methods

**SAT Encodings**
- Pairwise
- Bitwise
- Sequential Counter

**Solvers**
- PySAT
- CPLEX MIP
- CPLEX CP
- Gurobi
- OR-Tools CP-SAT

## Experiments

Two experiments are conducted:

1. Compare SAT encodings across different Sudoku board sizes.
2. Compare different solvers on Sudoku puzzles with varying clue levels.

Evaluation metrics include the number of variables and clauses, encoding time, solving time, and total execution time.

## Project Structure

- `src/`: Solver implementations and data generation.
- `experiments/`: Benchmark scripts.
- `data/`: Sudoku puzzles and benchmark results.
- `visualize/`: Notebooks for result visualization.

## Requirements

Python and the corresponding solver libraries are required. CPLEX and Gurobi may require separate installation and license configuration.

## Data Availability

Source code, datasets, benchmark results, and visualization notebooks are available in this repository.
