import time
import tkinter as tk
from src.core.node import Node
from src.ui.render import SudokuGUI

def run_step_by_step_demo(goal_node: Node, delay: float = 0.05):
    """
    Truy vết đường đi từ Node đích về Node gốc, sau đó dùng giao diện Tkinter
    để chiếu chậm (animation) từng bước AI điền số.
    """
    if not goal_node:
        print("Không có đường đi để hiển thị!")
        return
        
    # Truy vết đường đi
    path = []
    current = goal_node
    while current is not None:
        path.append(current)
        current = current.parent
        
    path.reverse() # Đảo ngược để đi từ Gốc -> Đích
    
    # Khởi tạo cửa sổ UI
    root = tk.Tk()
    gui = SudokuGUI(root, title=f"AI Solving... ({len(path) - 1} steps)")
    
    # Chạy vòng lặp in từng bảng
    print(f"\n=== BẮT ĐẦU DEMO ({len(path) - 1} bước) ===")
    for node in path:
        gui.update_board(node.state.board)
        time.sleep(delay) # Dừng một chút để tạo hiệu ứng animation
        
    print("=== HOÀN THÀNH DEMO ===")
    
    # Giữ cửa sổ không bị tắt ngay khi giải xong
    root.mainloop()