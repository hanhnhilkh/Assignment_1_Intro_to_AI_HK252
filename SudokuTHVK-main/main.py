import os
import sys

# Các lệnh import từ src
from src.sudoku.parser import load_puzzle
from src.sudoku.state import SudokuState
from src.core.blind import bfs
from src.core.heuristic import a_star
from src.core.metrics import measure_performance
from src.core.io_utils import append_to_benchmark
from src.sudoku.demo import run_step_by_step_demo

def print_board(board: tuple):
    """Hàm in Sudoku ra console một cách trực quan."""
    for i in range(9):
        if i % 3 == 0 and i != 0:
            print("- - - - - - - - - - - - -")
        row = board[i*9 : i*9+9]
        print(" ".join(str(x) if x != 0 else '.' for x in row[:3]) + " | " + 
              " ".join(str(x) if x != 0 else '.' for x in row[3:6]) + " | " + 
              " ".join(str(x) if x != 0 else '.' for x in row[6:]))
    print()

def main():
    # 1. Quét thư mục input và tạo Menu chọn file
    input_dir = "input"
    if not os.path.exists(input_dir):
        print(f"[-] Lỗi: Không tìm thấy thư mục '{input_dir}'")
        return
        
    txt_files = sorted([f for f in os.listdir(input_dir) if f.endswith('.txt')])
    
    if not txt_files:
        print(f"[-] Không có file .txt nào trong thư mục '{input_dir}'")
        return

    print("=== CHỌN BỘ INPUT SUDOKU ===")
    for i, file_name in enumerate(txt_files):
        print(f"[{i + 1}] {file_name}")
        
    try:
        choice = input("\nNhập số tương ứng với file bạn muốn chạy (hoặc bấm Enter để thoát): ")
        if not choice.strip():
            print("Đã thoát chương trình.")
            return
            
        choice_idx = int(choice) - 1
        if choice_idx < 0 or choice_idx >= len(txt_files):
            raise ValueError
            
        selected_file = txt_files[choice_idx]
        input_path = os.path.join(input_dir, selected_file)
    except ValueError:
        print("[-] Lựa chọn không hợp lệ! Vui lòng nhập đúng số trên menu.")
        return

    # 2. Bắt đầu chạy giải thuật với file đã chọn
    print(f"\n--- ĐANG TẢI SUDOKU TỪ: {input_path} ---")
    
    try:
        board_data = load_puzzle(input_path)
    except Exception as e:
        print(f"Lỗi khi đọc file: {e}")
        return

    initial_state = SudokuState(board_data)
    print("\n[ TRẠNG THÁI BAN ĐẦU ]")
    print_board(initial_state.board)
    empty_count = initial_state.board.count(0)
    
    # ==========================================
    # CHẠY BLIND SEARCH (BFS)
    # ==========================================
    if empty_count > 50:
        print(f"\n>>> BỎ QUA BLIND SEARCH (BFS)...")
        print(f"[-] Bài toán có {empty_count} ô trống. Quá khó để BFS giải quyết trong thời gian ngắn.")
    else:
        print("\n>>> ĐANG CHẠY BLIND SEARCH (BFS)...")
        (bfs_out, bfs_time, bfs_mem) = measure_performance(bfs, initial_state)
        bfs_goal_node, bfs_nodes_gen, bfs_max_nodes = bfs_out
        
        if bfs_goal_node:
            print("[+] BFS TÌM THẤY ĐÁP ÁN:")
            print_board(bfs_goal_node.state.board)
        else:
            print("[-] BFS không tìm thấy đáp án.")
            
        print(f"Thời gian (Runtime): {bfs_time:.4f} giây")
        print(f"Bộ nhớ RAM (Memory): {bfs_mem:.4f} MB")
        print(f"Số Node đã tạo:      {bfs_nodes_gen}")
        
        # Ghi vào file benchmark
        append_to_benchmark("benchmark.md", "BFS", selected_file, bfs_time, bfs_mem, bfs_nodes_gen)
    
    # ==========================================
    # CHẠY HEURISTIC SEARCH (A*)
    # ==========================================
    print("\n" + "="*40)
    print(">>> ĐANG CHẠY HEURISTIC SEARCH (A*)...")
    (astar_out, astar_time, astar_mem) = measure_performance(a_star, initial_state)
    astar_goal_node, astar_nodes_gen, astar_max_nodes = astar_out
    
    if astar_goal_node:
        print("[+] A* TÌM THẤY ĐÁP ÁN:")
        print_board(astar_goal_node.state.board)
    else:
        print("[-] A* không tìm thấy đáp án.")
        
    print(f"Thời gian (Runtime): {astar_time:.4f} giây")
    print(f"Bộ nhớ RAM (Memory): {astar_mem:.4f} MB")
    print(f"Số Node đã tạo:      {astar_nodes_gen}")
    
    # Ghi vào file benchmark
    append_to_benchmark("benchmark.md", "A*", selected_file, astar_time, astar_mem, astar_nodes_gen)

    # Khởi chạy giao diện UI
    if astar_goal_node:
        print("\n>>> ĐANG MỞ GIAO DIỆN DEMO...")
        run_step_by_step_demo(astar_goal_node, delay=0.05)

if __name__ == "__main__":
    main()