import tkinter as tk
from typing import Tuple

class SudokuGUI:
    def __init__(self, master: tk.Tk, title: str = "Sudoku AI Solver"):
        self.master = master
        self.master.title(title)
        
        # Kích thước mỗi ô vuông là 50px. Bảng 9x9 -> 450x450
        self.cell_size = 50
        self.width = self.cell_size * 9
        self.height = self.cell_size * 9
        
        # Tạo Canvas màu trắng
        self.canvas = tk.Canvas(self.master, width=self.width, height=self.height, bg='white')
        self.canvas.pack(padx=20, pady=20)
        
        self.draw_grid()

    def draw_grid(self):
        """Vẽ lưới Sudoku với các đường viền đậm cho khối 3x3 (giống ảnh của bạn)."""
        for i in range(10):
            # Nếu là đường chia khối 3x3 thì vẽ nét đậm (width=3), ngược lại nét mảnh (width=1)
            line_width = 3 if i % 3 == 0 else 1
            
            # Vẽ đường dọc
            x = i * self.cell_size
            self.canvas.create_line(x, 0, x, self.height, width=line_width, fill="black")
            
            # Vẽ đường ngang
            y = i * self.cell_size
            self.canvas.create_line(0, y, self.width, y, width=line_width, fill="black")

    def update_board(self, board: Tuple[int, ...]):
        """Cập nhật các con số lên bảng."""
        # Xóa các con số cũ trước khi vẽ số mới
        self.canvas.delete("numbers")
        
        for idx, val in enumerate(board):
            if val != 0:
                row = idx // 9
                col = idx % 9
                
                # Tính tọa độ tâm của ô
                x = col * self.cell_size + self.cell_size / 2
                y = row * self.cell_size + self.cell_size / 2
                
                # Số từ đề bài (màu đen), nếu bạn muốn làm phức tạp hơn thì tách màu số AI điền (màu xanh).
                # Ở đây ta tạm để màu đen/xanh đậm cho giống UI web.
                self.canvas.create_text(
                    x, y, 
                    text=str(val), 
                    font=("Helvetica", 20, "bold"), 
                    fill="#2c3e50",  # Màu xanh đen đẹp mắt
                    tags="numbers"
                )
        # Cập nhật giao diện ngay lập tức
        self.master.update()