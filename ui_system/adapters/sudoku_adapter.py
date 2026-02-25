import os
import sys
from dataclasses import dataclass
from typing import Any, List, Optional


@dataclass
class SudokuRunResult:
    goal_node: Optional[Any]
    nodes_generated: int
    max_memory_nodes: int
    time_sec: float
    memory_mb: float
    skipped: bool = False
    message: str = ""


class SudokuAdapter:
    """Thin wrapper around SudokuTHVK-main that does NOT modify its code.

    It imports and calls the original functions so BFS/A*/metrics/benchmark remain identical.
    """

    def __init__(self, sudoku_root: str):
        sudoku_root = os.path.abspath(sudoku_root)
        if not os.path.isdir(sudoku_root):
            raise FileNotFoundError(f"Sudoku root not found: {sudoku_root}")

        # Ensure imports like `from src...` inside SudokuTHVK-main resolve correctly.
        if sudoku_root not in sys.path:
            sys.path.insert(0, sudoku_root)

        #fix extra positional argument
        self.benchmark_file = os.path.join(sudoku_root, 'benchmark.md')

        from src.sudoku.parser import load_puzzle
        from src.sudoku.state import SudokuState
        from src.core.blind import bfs
        from src.core.heuristic import a_star
        from src.core.metrics import measure_performance
        from src.core.io_utils import append_to_benchmark

        self.load_puzzle = load_puzzle
        self.SudokuState = SudokuState
        self.bfs = bfs
        self.a_star = a_star
        self.measure_performance = measure_performance
        self.append_to_benchmark = append_to_benchmark

    def solve(self, input_path: str, algo: str, write_benchmark: bool = True) -> SudokuRunResult:
        algo_up = algo.strip().upper()
        if algo_up not in {"BFS", "A*", "ASTAR", "A STAR"}:
            raise ValueError("algo must be 'BFS' or 'A*'")
        algo_norm = "BFS" if algo_up == "BFS" else "A*"

        board = self.load_puzzle(input_path)
        init_state = self.SudokuState(board)

        # Keep the exact behavior from SudokuTHVK-main's main.py: skip BFS if too many empty cells.
        if algo_norm == "BFS":
            empty_count = sum(1 for x in board if x == 0)
            if empty_count > 50:
                return SudokuRunResult(
                    goal_node=None,
                    nodes_generated=0,
                    max_memory_nodes=0,
                    time_sec=0.0,
                    memory_mb=0.0,
                    skipped=True,
                    message="BFS skipped (more than 50 empty cells).",
                )

            (res, t, mem) = self.measure_performance(self.bfs, init_state)
            goal_node, nodes_gen, max_mem_nodes = res
        else:
            (res, t, mem) = self.measure_performance(self.a_star, init_state)
            goal_node, nodes_gen, max_mem_nodes = res

        if write_benchmark:
            puzzle_name = os.path.basename(input_path)
            #fix extra positional argument
            self.append_to_benchmark(
                self.benchmark_file,
                algo_norm,
                puzzle_name,
                t,
                mem,
                nodes_gen,            
            )

        msg = "Solved" if goal_node else "No solution found"
        return SudokuRunResult(goal_node, nodes_gen, max_mem_nodes, t, mem, skipped=False, message=msg)

    @staticmethod
    def reconstruct_nodes(goal_node: Any) -> List[Any]:
        nodes: List[Any] = []
        cur = goal_node
        while cur is not None:
            nodes.append(cur)
            cur = getattr(cur, "parent", None)
        nodes.reverse()
        return nodes

    @staticmethod
    def nodes_to_boards(nodes: List[Any]) -> List[Any]:
        boards = []
        for n in nodes:
            st = getattr(n, "state", None)
            boards.append(getattr(st, "board", None))
        return boards
