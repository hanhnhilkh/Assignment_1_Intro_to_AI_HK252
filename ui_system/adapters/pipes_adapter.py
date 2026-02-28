import os
import importlib.util
from dataclasses import dataclass
from typing import Optional, Tuple, Any, List, Dict


@dataclass
class PipesRunResult:
    goal_state: Any
    path_states: Optional[List[Any]]
    stats: Dict[str, Any]


class PipesAdapter:
    """
    Adapter (wrapper) to call the group's 7x7 Wrap Pipes solver without modifying their code.
    We load the solver module from 7x7-pipes-wrap-main/main.py via importlib to avoid name clashes.
    """

    def __init__(self, pipes_root: str):
        self.pipes_root = pipes_root
        main_py = os.path.join(pipes_root, "main.py")
        if not os.path.isfile(main_py):
            raise FileNotFoundError(f"Cannot find pipes main.py at: {main_py}")

        spec = importlib.util.spec_from_file_location("pipes_main_module", main_py)
        mod = importlib.util.module_from_spec(spec)
        assert spec.loader is not None
        spec.loader.exec_module(mod)

        self.mod = mod  # keep reference
        self.PipeState = mod.PipeState

    def load_puzzle_from_file(self, path: str):
        with open(path, "r", encoding="utf-8") as f:
            content = f.read()
        return self.PipeState.from_string(content)

    #bfs, dfs, a*, hill climbing
    def solve(self, initial_state, algo: str) -> PipesRunResult:
        algo_norm = algo.strip().upper()
        if algo_norm == "BFS":
            goal, path, stats = self.mod.bfs(initial_state)
        elif algo_norm == "A*":
            goal, path, stats = self.mod.astar(initial_state)
        elif algo_norm == "HILL CLIMBING":
            goal, path, stats = self.mod.hill_climbing(initial_state)
        else:
            # DFS has optional show_progress
            goal, path, stats = self.mod.dfs(initial_state)
        return PipesRunResult(goal, path, stats)
