import os

def append_to_benchmark(filename: str, algorithm: str, puzzle_name: str, time_sec: float, memory_mb: float, nodes: int):
    """Ghi thêm một dòng kết quả đo lường vào file Markdown để tạo bảng chuyên nghiệp."""
    file_exists = os.path.isfile(filename)
    
    with open(filename, mode='a', encoding='utf-8') as f:
        # Ghi Header của bảng nếu file chưa tồn tại hoặc bị trống
        if not file_exists or os.path.getsize(filename) == 0:
            f.write("## 📊 Sudoku Benchmark Results\n\n")
            f.write("| Algorithm | Puzzle Name  | Time (s) | Memory (MB) | Nodes Generated |\n")
            f.write("|:---------:|:-------------|---------:|------------:|----------------:|\n")
        
        # Ghi dữ liệu với padding (khoảng trắng) để các cột luôn thẳng hàng nhau khi xem dạng text
        f.write(f"| {algorithm:^9} | {puzzle_name:<12} | {time_sec:>8.5f} | {memory_mb:>11.5f} | {nodes:>15} |\n")