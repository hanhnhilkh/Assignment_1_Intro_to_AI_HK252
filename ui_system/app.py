import os
import tkinter as tk
from tkinter import filedialog, messagebox, ttk

from adapters.sudoku_adapter import SudokuAdapter
from adapters.pipes_adapter import PipesAdapter
from widgets.sudoku_board import SudokuBoard
from widgets.pipes_board import PipesBoard


class MainMenu(tk.Frame):
    def __init__(self, master, on_select_game):
        super().__init__(master)
        self.on_select_game = on_select_game

        self.columnconfigure(0, weight=1)

        title = tk.Label(self, text="AI Puzzles - Main Menu", font=("Arial", 20, "bold"))
        title.grid(row=0, column=0, pady=(30, 10), padx=20)

        subtitle = tk.Label(
            self,
            text="Choose a game to open its UI.",
            font=("Arial", 12),
        )
        subtitle.grid(row=1, column=0, pady=(0, 30), padx=20)

        btn_sudoku = tk.Button(self, text="Sudoku", font=("Arial", 14), width=18, command=lambda: self.on_select_game("sudoku"))
        btn_sudoku.grid(row=2, column=0, pady=10)

        btn_pipes = tk.Button(self, text="Wrap Pipes", font=("Arial", 14), width=18, command=lambda: self.on_select_game("pipes"))
        btn_pipes.grid(row=3, column=0, pady=10)

        note = tk.Label(
            self,
            text="Wrap Pipes: rotate pipes so the whole network is connected (wrap-around edges).",
            font=("Arial", 10),
        )
        note.grid(row=4, column=0, pady=(25, 0), padx=20)


class SudokuScreen(tk.Frame):
    def __init__(self, master, on_back, project_root):
        super().__init__(master)
        self.on_back = on_back
        self.project_root = project_root

        self.sudoku_root = os.path.join(project_root, "SudokuTHVK-main")
        self.adapter = None

        self.steps = []  # list[tuple[int,...]]
        self.step_idx = 0
        self._auto_job = None

        self._build_ui()
        self._init_adapter()

    def _build_ui(self):
        # Top bar
        top = tk.Frame(self)
        top.pack(fill="x", padx=12, pady=10)

        tk.Button(top, text="← Back", command=self._back).pack(side="left")
        tk.Label(top, text="Sudoku", font=("Arial", 16, "bold")).pack(side="left", padx=12)

        # Body split
        body = tk.Frame(self)
        body.pack(fill="both", expand=True, padx=12, pady=12)

        left = tk.Frame(body)
        left.pack(side="left", fill="y")

        right = tk.Frame(body)
        right.pack(side="left", fill="both", expand=True, padx=(16, 0))

        # Controls (left)
        ctrl = tk.LabelFrame(left, text="Controls", padx=10, pady=10)
        ctrl.pack(fill="x")

        # Input
        row = tk.Frame(ctrl)
        row.pack(fill="x", pady=(0, 8))
        tk.Label(row, text="Input file:").pack(side="left")
        self.input_var = tk.StringVar(value="")
        self.input_entry = tk.Entry(row, textvariable=self.input_var, width=28)
        self.input_entry.pack(side="left", padx=6)
        tk.Button(row, text="Browse…", command=self._browse).pack(side="left")

        # Algo select
        row2 = tk.Frame(ctrl)
        row2.pack(fill="x", pady=(0, 8))
        tk.Label(row2, text="Algorithm:").pack(side="left")
        self.algo_var = tk.StringVar(value="A*")
        algo_box = ttk.Combobox(row2, textvariable=self.algo_var, values=["A*", "BFS"], state="readonly", width=8)
        algo_box.pack(side="left", padx=6)

        # Delay
        row3 = tk.Frame(ctrl)
        row3.pack(fill="x", pady=(0, 8))
        tk.Label(row3, text="Auto delay (ms):").pack(side="left")
        self.delay_var = tk.StringVar(value="120")
        tk.Entry(row3, textvariable=self.delay_var, width=8).pack(side="left", padx=6)

        # Buttons
        btns = tk.Frame(ctrl)
        btns.pack(fill="x", pady=(6, 0))

        self.btn_solve = tk.Button(btns, text="Solve", width=10, command=self._solve)
        self.btn_solve.grid(row=0, column=0, padx=3, pady=3)

        self.btn_step = tk.Button(btns, text="Step", width=10, command=self._step, state="disabled")
        self.btn_step.grid(row=0, column=1, padx=3, pady=3)

        self.btn_auto = tk.Button(btns, text="Auto", width=10, command=self._toggle_auto, state="disabled")
        self.btn_auto.grid(row=0, column=2, padx=3, pady=3)

        self.btn_reset = tk.Button(btns, text="Reset", width=10, command=self._reset, state="disabled")
        self.btn_reset.grid(row=1, column=0, padx=3, pady=3)

        self.btn_clear = tk.Button(btns, text="Clear", width=10, command=self._clear)
        self.btn_clear.grid(row=1, column=1, padx=3, pady=3)

        # Stats
        stats = tk.LabelFrame(left, text="Stats", padx=10, pady=10)
        stats.pack(fill="x", pady=(12, 0))

        self.stats_text = tk.Text(stats, width=38, height=12, wrap="word")
        self.stats_text.pack(fill="both", expand=True)
        self._set_stats("Choose an input file, then click Solve.")

        # Board (right)
        board_frame = tk.Frame(right)
        board_frame.pack(fill="both", expand=True)

        self.board = SudokuBoard(board_frame, cell_size=55, pad=10)
        self.board.pack()

        hint = tk.Label(right, text="Tip: Use A* for harder puzzles. BFS is skipped when > 50 empty cells.")
        hint.pack(anchor="w", pady=(10, 0))

    def _init_adapter(self):
        try:
            self.adapter = SudokuAdapter(self.sudoku_root)
        except Exception as e:
            messagebox.showerror("Sudoku Adapter Error", str(e))
            self.adapter = None

    def _browse(self):
        path = filedialog.askopenfilename(
            title="Choose Sudoku .txt",
            filetypes=[("Text files", "*.txt"), ("All files", "*")],
        )
        if path:
            self.input_var.set(path)
            # show initial board
            self._load_and_render_initial(path)

    def _load_and_render_initial(self, path: str):
        if not self.adapter:
            return
        try:
            board = self.adapter.load_puzzle(path)
        except Exception as e:
            messagebox.showerror("Input Error", f"Failed to load puzzle:\n{e}")
            return
        self._stop_auto()
        self.steps = [tuple(board)]
        self.step_idx = 0
        self.board.render(self.steps[0])
        self.btn_step.configure(state="disabled")
        self.btn_auto.configure(state="disabled")
        self.btn_reset.configure(state="disabled")
        self._set_stats("Loaded puzzle. Click Solve to run the algorithm.")

    def _solve(self):
        if not self.adapter:
            return

        path = self.input_var.get().strip()
        if not path:
            messagebox.showwarning("Missing input", "Please choose a .txt input file.")
            return
        if not os.path.isfile(path):
            messagebox.showwarning("Invalid input", "Selected input file does not exist.")
            return

        algo = self.algo_var.get().strip()
        self._stop_auto()
        self._set_stats("Running...")
        self.update_idletasks()

        try:
            res = self.adapter.solve(path, algo, write_benchmark=True)
        except Exception as e:
            messagebox.showerror("Solve Error", str(e))
            self._set_stats("Solve failed.")
            return

        if res.skipped:
            self._set_stats(
                f"{res.message}\n\n"
                f"Algorithm: {algo}\n"
                f"Time: {res.time_sec:.6f}s\n"
                f"Peak memory: {res.memory_mb:.3f} MB\n"
                f"Nodes generated: {res.nodes_generated}\n"
                f"Max memory nodes: {res.max_memory_nodes}\n"
            )
            return

        if not res.goal_node:
            self._set_stats(
                f"No solution found.\n\n"
                f"Algorithm: {algo}\n"
                f"Time: {res.time_sec:.6f}s\n"
                f"Peak memory: {res.memory_mb:.3f} MB\n"
                f"Nodes generated: {res.nodes_generated}\n"
                f"Max memory nodes: {res.max_memory_nodes}\n"
            )
            return

        nodes = self.adapter.reconstruct_nodes(res.goal_node)
        boards = self.adapter.nodes_to_boards(nodes)
        boards = [tuple(b) for b in boards if b is not None]

        self.steps = boards
        self.step_idx = 0
        self.board.render(self.steps[0])

        self.btn_step.configure(state="normal")
        self.btn_auto.configure(state="normal")
        self.btn_reset.configure(state="normal")

        self._set_stats(
            f"Solved!\n\n"
            f"Algorithm: {algo}\n"
            f"Steps: {len(self.steps) - 1}\n"
            f"Time: {res.time_sec:.6f}s\n"
            f"Peak memory: {res.memory_mb:.3f} MB\n"
            f"Nodes generated: {res.nodes_generated}\n"
            f"Max memory nodes: {res.max_memory_nodes}\n\n"
            f"Benchmark appended in SudokuTHVK-main/benchmark.md"
        )

    def _step(self):
        if not self.steps:
            return
        if self.step_idx >= len(self.steps) - 1:
            self._stop_auto()
            return

        prev = self.steps[self.step_idx]
        self.step_idx += 1
        cur = self.steps[self.step_idx]
        hl = SudokuBoard.diff_cell(prev, cur)
        self.board.render(cur, highlight=hl)

        if self.step_idx >= len(self.steps) - 1:
            self._stop_auto()

    def _toggle_auto(self):
        if self._auto_job is not None:
            self._stop_auto()
            return

        delay = 120
        try:
            delay = max(10, int(self.delay_var.get().strip()))
        except Exception:
            delay = 120
            self.delay_var.set("120")

        self.btn_auto.configure(text="Stop")

        def tick():
            self._auto_job = self.after(delay, tick)
            self._step()

        self._auto_job = self.after(delay, tick)

    def _stop_auto(self):
        if self._auto_job is not None:
            try:
                self.after_cancel(self._auto_job)
            except Exception:
                pass
        self._auto_job = None
        self.btn_auto.configure(text="Auto")

    def _reset(self):
        if not self.steps:
            return
        self._stop_auto()
        self.step_idx = 0
        self.board.render(self.steps[0])

    def _clear(self):
        self._stop_auto()
        self.steps = []
        self.step_idx = 0
        self.board.delete("numbers")
        self.board.delete("hl")
        self._set_stats("Cleared. Choose an input file.")
        self.btn_step.configure(state="disabled")
        self.btn_auto.configure(state="disabled")
        self.btn_reset.configure(state="disabled")

    def _set_stats(self, text: str):
        self.stats_text.configure(state="normal")
        self.stats_text.delete("1.0", "end")
        self.stats_text.insert("1.0", text)
        self.stats_text.configure(state="disabled")

    def _back(self):
        self._stop_auto()
        self.on_back()




class PipesScreen(tk.Frame):
    def __init__(self, master, on_back, project_root):
        super().__init__(master)
        self.on_back = on_back
        self.project_root = project_root

        self.pipes_root = os.path.join(project_root, "7x7-pipes-wrap-main")
        self.adapter = None

        self.steps = []  # list[PipeState]
        self.step_idx = 0
        self._auto_job = None

        self._build_ui()
        self._init_adapter()

    def _build_ui(self):
        # Top bar
        top = tk.Frame(self)
        top.pack(fill="x", padx=12, pady=10)

        tk.Button(top, text="← Back", command=self._back).pack(side="left")
        tk.Label(top, text="Wrap Pipes (7x7)", font=("Arial", 16, "bold")).pack(side="left", padx=12)

        # Body split
        body = tk.Frame(self)
        body.pack(fill="both", expand=True, padx=12, pady=12)

        left = tk.Frame(body)
        left.pack(side="left", fill="y")

        right = tk.Frame(body)
        right.pack(side="left", fill="both", expand=True, padx=(16, 0))

        # Controls
        ctrl = tk.LabelFrame(left, text="Controls", padx=10, pady=10)
        ctrl.pack(fill="x")

        row = tk.Frame(ctrl)
        row.pack(fill="x", pady=(0, 8))
        tk.Label(row, text="Input file:").pack(side="left")
        self.input_var = tk.StringVar(value="")
        self.input_entry = tk.Entry(row, textvariable=self.input_var, width=28)
        self.input_entry.pack(side="left", padx=6)
        tk.Button(row, text="Browse…", command=self._browse).pack(side="left")

        row2 = tk.Frame(ctrl)
        row2.pack(fill="x", pady=(0, 8))
        tk.Label(row2, text="Algorithm:").pack(side="left")
        self.algo_var = tk.StringVar(value="BFS")
        algo_box = ttk.Combobox(row2, textvariable=self.algo_var, values=["A*", "BFS", "DFS", "Hill Climbing"], state="readonly", width=8)
        algo_box.pack(side="left", padx=6)

        row3 = tk.Frame(ctrl)
        row3.pack(fill="x", pady=(0, 8))
        tk.Label(row3, text="Auto delay (ms):").pack(side="left")
        self.delay_var = tk.StringVar(value="120")
        tk.Entry(row3, textvariable=self.delay_var, width=8).pack(side="left", padx=6)

        btns = tk.Frame(ctrl)
        btns.pack(fill="x", pady=(6, 0))

        self.btn_solve = tk.Button(btns, text="Solve", width=10, command=self._solve)
        self.btn_solve.grid(row=0, column=0, padx=3, pady=3)

        self.btn_step = tk.Button(btns, text="Step", width=10, command=self._step, state="disabled")
        self.btn_step.grid(row=0, column=1, padx=3, pady=3)

        self.btn_auto = tk.Button(btns, text="Auto", width=10, command=self._toggle_auto, state="disabled")
        self.btn_auto.grid(row=0, column=2, padx=3, pady=3)

        self.btn_reset = tk.Button(btns, text="Reset", width=10, command=self._reset, state="disabled")
        self.btn_reset.grid(row=1, column=0, padx=3, pady=3)

        self.btn_clear = tk.Button(btns, text="Clear", width=10, command=self._clear)
        self.btn_clear.grid(row=1, column=1, padx=3, pady=3)

        stats = tk.LabelFrame(left, text="Stats", padx=10, pady=10)
        stats.pack(fill="x", pady=(12, 0))

        self.stats_text = tk.Text(stats, width=38, height=12, wrap="word")
        self.stats_text.pack(fill="both", expand=True)
        self._set_stats("Choose an input file, then click Solve.")

        board_frame = tk.Frame(right)
        board_frame.pack(fill="both", expand=True)

        self.board = PipesBoard(board_frame, cell_size=55, pad=10)
        self.board.pack()

        hint = tk.Label(
            right,
            text="Goal: rotate tiles to make one connected network, with wrap-around edges.",
        )
        hint.pack(anchor="w", pady=(10, 0))

    def _init_adapter(self):
        try:
            self.adapter = PipesAdapter(self.pipes_root)
        except Exception as e:
            messagebox.showerror("Pipes Adapter Error", str(e))
            self.adapter = None

    def _browse(self):
        path = filedialog.askopenfilename(
            title="Choose Pipes .txt",
            filetypes=[("Text files", "*.txt"), ("All files", "*")],
        )
        if path:
            self.input_var.set(path)
            self._load_and_render_initial(path)

    def _load_and_render_initial(self, path: str):
        if not self.adapter:
            return
        try:
            init_state = self.adapter.load_puzzle_from_file(path)
        except Exception as e:
            messagebox.showerror("Input Error", f"Failed to load pipes:\n{e}")
            return
        self._stop_auto()
        self.steps = [init_state]
        self.step_idx = 0
        self.board.render(self.steps[0])
        self.btn_step.configure(state="disabled")
        self.btn_auto.configure(state="disabled")
        self.btn_reset.configure(state="disabled")
        self._set_stats("Loaded puzzle. Click Solve to run the algorithm.")

    def _solve(self):
        if not self.adapter:
            return
        path = self.input_var.get().strip()
        if not path:
            messagebox.showwarning("Missing input", "Please choose an input file.")
            return

        try:
            init_state = self.adapter.load_puzzle_from_file(path)
        except Exception as e:
            messagebox.showerror("Input Error", f"Failed to load pipes:\n{e}")
            return

        algo = self.algo_var.get().strip()
        # algo_norm = "DFS" if algo.upper().startswith("D") else "BFS"
        if algo.upper().startswith("A"):
            algo_norm = "A*"
        elif algo.upper().startswith("H"):
            algo_norm = "HILL CLIMBING"
        elif algo.upper().startswith("B"):
            algo_norm = "BFS"
        else:
            algo_norm = "DFS"

        self._stop_auto()
        self._set_stats("Solving...")

        try:
            res = self.adapter.solve(init_state, algo_norm)
        except Exception as e:
            messagebox.showerror("Solve Error", str(e))
            self._set_stats("Solve failed.")
            return

        if not res.path_states:
            self.steps = [init_state]
            self.step_idx = 0
            self.board.render(init_state)
            self.btn_step.configure(state="disabled")
            self.btn_auto.configure(state="disabled")
            self.btn_reset.configure(state="disabled")
            self._set_stats(f"No solution found.\n\nStats:\n{self._format_pipes_stats(res.stats)}")
            return

        self.steps = res.path_states
        self.step_idx = 0
        self.board.render(self.steps[0])
        self.btn_step.configure(state="normal")
        self.btn_auto.configure(state="normal")
        self.btn_reset.configure(state="normal")
        self._set_stats(f"Solved! Steps: {len(self.steps)-1}\n\nStats:\n{self._format_pipes_stats(res.stats)}")

    def _format_pipes_stats(self, stats: dict) -> str:
        # stats keys depend on the group's code; handle missing keys safely
        lines = []
        for k in ["nodes_explored", "nodes_generated", "max_frontier_size", "visited_states"]:
            if k in stats:
                lines.append(f"- {k}: {stats[k]}")
        # Some versions may include time/memory; show if present
        for k in ["time_sec", "memory_mb"]:
            if k in stats:
                lines.append(f"- {k}: {stats[k]}")
        if not lines:
            lines.append(str(stats))
        return "\n".join(lines)

    def _step(self):
        if not self.steps or self.step_idx >= len(self.steps) - 1:
            return
        prev = self.steps[self.step_idx]
        self.step_idx += 1
        cur = self.steps[self.step_idx]
        hi = self._diff_cell(prev, cur)
        self.board.render(cur, highlight=hi)
        self._set_stats(f"Step {self.step_idx}/{len(self.steps)-1}")

    def _toggle_auto(self):
        if self._auto_job is None:
            self.btn_auto.configure(text="Stop")
            self._auto_next()
        else:
            self._stop_auto()

    def _auto_next(self):
        if self.step_idx >= len(self.steps) - 1:
            self._stop_auto()
            return
        try:
            delay = int(self.delay_var.get().strip())
        except Exception:
            delay = 120
        self._step()
        self._auto_job = self.after(max(1, delay), self._auto_next)

    def _stop_auto(self):
        if self._auto_job is not None:
            try:
                self.after_cancel(self._auto_job)
            except Exception:
                pass
        self._auto_job = None
        self.btn_auto.configure(text="Auto")

    def _reset(self):
        if not self.steps:
            return
        self._stop_auto()
        self.step_idx = 0
        self.board.render(self.steps[0])
        self._set_stats("Reset to initial state.")

    def _clear(self):
        self._stop_auto()
        self.steps = []
        self.step_idx = 0
        self.input_var.set("")
        self.board.clear()
        self.btn_step.configure(state="disabled")
        self.btn_auto.configure(state="disabled")
        self.btn_reset.configure(state="disabled")
        self._set_stats("Choose an input file, then click Solve.")

    def _diff_cell(self, a_state, b_state):
        try:
            ga = a_state.grid
            gb = b_state.grid
            n = len(ga)
            for r in range(n):
                for c in range(n):
                    ta = ga[r][c]
                    tb = gb[r][c]
                    if ta != tb:
                        return (r, c)
        except Exception:
            return None
        return None

    def _set_stats(self, text: str):
        self.stats_text.configure(state="normal")
        self.stats_text.delete("1.0", "end")
        self.stats_text.insert("1.0", text)
        self.stats_text.configure(state="disabled")

    def _back(self):
        self._stop_auto()
        self.on_back()


class App(tk.Tk):
    def __init__(self, project_root: str):
        super().__init__()
        self.title("AI Puzzles UI")
        self.geometry("980x720")

        self.project_root = os.path.abspath(project_root)

        self.container = tk.Frame(self)
        self.container.pack(fill="both", expand=True)

        self.menu = MainMenu(self.container, self._open_game)
        self.menu.pack(fill="both", expand=True)

        self.current_screen = None

    def _open_game(self, game_key: str):
        if self.current_screen is not None:
            self.current_screen.destroy()
            self.current_screen = None

        self.menu.pack_forget()

        if game_key == "sudoku":
            self.current_screen = SudokuScreen(self.container, on_back=self._go_menu, project_root=self.project_root)
            self.current_screen.pack(fill="both", expand=True)
        else:
            self.current_screen = PipesScreen(self.container, on_back=self._go_menu, project_root=self.project_root)
            self.current_screen.pack(fill="both", expand=True)

    def _go_menu(self):
        if self.current_screen is not None:
            self.current_screen.destroy()
            self.current_screen = None
        self.menu.pack(fill="both", expand=True)


def main():
    # project/
    #   |-7x7-pipes-wrap-main/
    #   |-SudokuTHVK-main/
    #   |-ui_system/
    project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
    app = App(project_root=project_root)
    app.mainloop()


if __name__ == "__main__":
    main()
