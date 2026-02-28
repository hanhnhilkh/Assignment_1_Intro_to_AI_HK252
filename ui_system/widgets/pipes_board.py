import tkinter as tk
from typing import Any, Optional, Tuple


class PipesBoard(tk.Canvas):
    """
    Simple renderer for the 7x7 Wrap Pipes board.
    Expects a PipeState with:
      - state.grid: 2D list of Tile objects
      - tile.to_char(): returns a unicode char representing the pipe shape
    """
    def __init__(self, master, cell_size: int = 60, pad: int = 10):
        self.cell_size = cell_size
        self.pad = pad
        # 7x7 default
        w = pad * 2 + cell_size * 7
        h = pad * 2 + cell_size * 7
        super().__init__(master, width=w, height=h, bg="white", highlightthickness=0)
        self._last_state = None

    def clear(self):
        self.delete("all")
        self._last_state = None

    def render(self, state: Any, highlight: Optional[Tuple[int, int]] = None):
        self.delete("all")
        if state is None:
            return

        grid = state.grid
        n = len(grid)

        # grid lines
        for r in range(n + 1):
            y = self.pad + r * self.cell_size
            self.create_line(self.pad, y, self.pad + n * self.cell_size, y)
        for c in range(n + 1):
            x = self.pad + c * self.cell_size
            self.create_line(x, self.pad, x, self.pad + n * self.cell_size)

        # highlight cell (changed tile)
        if highlight is not None:
            r, c = highlight
            x0 = self.pad + c * self.cell_size
            y0 = self.pad + r * self.cell_size
            x1 = x0 + self.cell_size
            y1 = y0 + self.cell_size
            self.create_rectangle(x0, y0, x1, y1, outline="", fill="#fff2a8")

        # draw tiles
        font_size = max(12, int(self.cell_size * 0.55))
        for r in range(n):
            for c in range(n):
                tile = grid[r][c]
                ch = tile.to_char() if hasattr(tile, "to_char") else str(tile)
                x = self.pad + c * self.cell_size + self.cell_size / 2
                y = self.pad + r * self.cell_size + self.cell_size / 2
                self.create_text(x, y, text=ch, font=("Arial", font_size))
