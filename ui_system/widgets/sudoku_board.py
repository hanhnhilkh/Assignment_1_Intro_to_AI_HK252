import tkinter as tk
from typing import Optional, Sequence, Tuple


class SudokuBoard(tk.Canvas):
    def __init__(
        self,
        master,
        cell_size: int = 55,
        pad: int = 10,
        **kwargs,
    ):
        self.cell_size = cell_size
        self.pad = pad
        w = pad * 2 + cell_size * 9
        h = pad * 2 + cell_size * 9
        super().__init__(master, width=w, height=h, highlightthickness=0, **kwargs)

        self._board: Optional[Tuple[int, ...]] = None
        self._draw_grid()

    def _draw_grid(self):
        self.delete("grid")
        p = self.pad
        cs = self.cell_size

        # Background
        self.create_rectangle(0, 0, p * 2 + cs * 9, p * 2 + cs * 9, fill="white", outline="", tags="grid")

        # Grid lines (thin + thick)
        for i in range(10):
            x0 = p + i * cs
            y0 = p + i * cs
            width = 3 if i % 3 == 0 else 1
            self.create_line(p, y0, p + 9 * cs, y0, width=width, fill="black", tags="grid")
            self.create_line(x0, p, x0, p + 9 * cs, width=width, fill="black", tags="grid")

    def render(self, board: Sequence[int], highlight: Optional[Tuple[int, int]] = None):
        """Render a 9x9 board (length 81). highlight is (r,c) to highlight the cell."""
        self._board = tuple(board)
        self.delete("numbers")
        self.delete("hl")

        p = self.pad
        cs = self.cell_size

        if highlight is not None:
            r, c = highlight
            x1 = p + c * cs
            y1 = p + r * cs
            x2 = x1 + cs
            y2 = y1 + cs
            self.create_rectangle(x1 + 1, y1 + 1, x2 - 1, y2 - 1, outline="", fill="#ffeaa7", tags="hl")

        for idx, val in enumerate(self._board):
            if val == 0:
                continue
            r, c = divmod(idx, 9)
            x = p + c * cs + cs / 2
            y = p + r * cs + cs / 2
            self.create_text(x, y, text=str(val), font=("Arial", int(cs * 0.4), "bold"), tags="numbers")

    @staticmethod
    def diff_cell(prev_board: Optional[Sequence[int]], cur_board: Sequence[int]) -> Optional[Tuple[int, int]]:
        if prev_board is None:
            return None
        for i, (a, b) in enumerate(zip(prev_board, cur_board)):
            if a != b:
                return divmod(i, 9)
        return None
