# AI Puzzles

Tkinter UI wrapper for the Sudoku and 7x7 wrap pipes game solvers. 

## Setup
We recommend using a virtual environment.

```bash
python -m venv .venv
# Windows
.venv\Scripts\activate

# macOS/Linux
source .venv/bin/activate
```

No extra dependencies required (Tkinter is included with most Python installations).

## Run

From the project root:

python ui_system/app.py

## How to play / solve Sudoku

Open Sudoku from the main menu.

Click Browse to select a .txt puzzle file.

Choose an algorithm (BFS or A*), then click Solve.

Use Step or Auto to replay the solution.

## How to play / solve 7x7 wrap pipes

## Notes

BFS is skipped automatically when the puzzle has more than 50 empty cells (same rule as SudokuTHVK-main).

Results are appended to SudokuTHVK-main/benchmark.md.
