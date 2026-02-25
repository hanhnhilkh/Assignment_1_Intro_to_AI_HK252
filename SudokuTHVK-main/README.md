# SudokuTHVK
BTL1 - Introduction to Artificial Intelligence Sudoku (Blind Search &amp; Heuristic Search) 

This project implements a single logic puzzle game (Sudoku 9x9) using
two search approaches:
- Blind Search: Breadth-First Search (BFS)
- Heuristic Search: A* Search

The source code is organized into a core search framework and a
Sudoku-specific module that defines state representation, successor
generation, and heuristic functions. Input test cases, experimental
outputs, and the final report are separated for clarity and evaluation.

Project Structure:
SudokuTHVK/
│
├── .gitignore
├── README.md
├── requirements.txt
│
├── src/
│   ├── main.py                     # Entry point: chạy chương trình
│   │
│   ├── core/                       # Framework tìm kiếm (dùng chung)
│   │   ├── node.py                 # Node: state, parent, g, h, f
│   │   ├── searchs.py  (isoleted)  # BFS (Blind) & A* (Heuristic)
│   │   ├── blind.py                # BFS
│   │   ├── heuristic.py            # A* searching
│   │   ├── metrics.py              # Đo time, RAM, số node mở rộng
│   │   ├── io_utils.py             # Đọc input / ghi output
│   │   └── __init__.py             #nothing here bud
│   │
│   ├── sudoku/                     # Game duy nhất: Sudoku 9x9
│   │   ├── state.py                # SudokuState, is_goal, get_successors
│   │   ├── rules.py                # Ràng buộc Sudoku, candidates, MRV
│   │   ├── heuristic_rule.py            # Heuristic h(n) cho A*
│   │   ├── parser.py               # Parse input Sudoku
│   │   ├── demo.py                 # Hiển thị từng bước (text-based)
│   │   └── __init__.py              
│   │
│   └── ui/
│       ├── cli.py                  # Menu chọn thuật toán & input
│       ├── render.py               # In Sudoku board đẹp
│       └── __init__.py
│
├── input/
│   └── sudoku/
│       ├── easy_01.txt
│       ├── medium_01.txt
│       └── hard_01.txt
│
├──── benchmark.csv                  # Kết quả đo time & memory
│
└── report/
    ├── report.docx (hoặc pdf)
    └── figures/                    # Hình minh hoạ / biểu đồ

    Lệnh chạy: python main.py
    chọn file để chạy theo số thứ tự và name ( type: 1,2,3,4 )