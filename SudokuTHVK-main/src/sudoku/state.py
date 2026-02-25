from typing import List, Tuple, Callable, Optional
from .rules import get_candidates, find_empty_cells, EMPTY, select_unassigned_cell_mrv

def select_first_unassigned_cell(board: Tuple[int, ...]) -> Optional[int]:
    """
    Dành cho Blind Search (BFS): Chọn ô trống đầu tiên từ trái sang phải, trên xuống dưới.
    Không dùng bất kỳ heuristic nào.
    """
    empties = find_empty_cells(board)
    return empties[0] if empties else None


class SudokuState:
    def __init__(self, board: Tuple[int, ...]):
        """
        Khởi tạo trạng thái Sudoku.
        board: Một tuple gồm 81 số nguyên (0 biểu diễn ô trống).
        Sử dụng tuple giúp State trở thành bất biến (immutable) và dễ dàng băm (hash).
        """
        self.board = board

    def is_goal(self) -> bool:
        """
        Kiểm tra xem trạng thái hiện tại đã là đích chưa.
        Do hàm sinh successors luôn đảm bảo luật Sudoku (thông qua get_candidates),
        nên trạng thái đích đơn giản là trạng thái không còn ô trống nào.
        """
        return EMPTY not in self.board

    def get_successors(self, select_cell_fn: Callable[[Tuple[int, ...]], Optional[int]] = select_first_unassigned_cell) -> List['SudokuState']:
        """
        Sinh ra các trạng thái con hợp lệ từ trạng thái hiện tại.
        
        Tham số:
            - select_cell_fn: Hàm quyết định xem sẽ chọn ô trống nào để điền tiếp theo.
              + Truền `select_first_unassigned_cell` khi chạy BFS.
              + Truyền `select_unassigned_cell_mrv` khi chạy A* để thu hẹp cây tìm kiếm.
        """
        successors: List['SudokuState'] = []

        # 1. Chọn ô trống cần điền dựa theo chiến lược truyền vào
        idx = select_cell_fn(self.board)

        # Nếu không còn ô trống nào, trạng thái không thể mở rộng thêm
        if idx is None:
            return successors

        # 2. Lấy các giá trị hợp lệ có thể điền vào ô `idx` này
        candidates = get_candidates(self.board, idx)

        # 3. Tạo các trạng thái con (child states) cho mỗi ứng viên hợp lệ
        for val in candidates:
            # Chuyển tuple thành list để có thể gán giá trị mới
            new_board_list = list(self.board)
            new_board_list[idx] = val
            # Chuyển lại thành tuple để giữ tính bất biến
            new_board = tuple(new_board_list)
            
            # Thêm trạng thái con mới vào danh sách
            successors.append(SudokuState(new_board))

        return successors

    def __eq__(self, other: object) -> bool:
        """ 
        Định nghĩa phép so sánh bằng. Rất cần thiết khi thuật toán tìm kiếm 
        cần kiểm tra xem state này đã nằm trong explored set (closed list) hay chưa.
        """
        if not isinstance(other, SudokuState):
            return False
        return self.board == other.board

    def __hash__(self) -> int:
        """
        Định nghĩa hàm băm (hash). 
        Cho phép đưa đối tượng SudokuState vào set() hoặc dict() trong các file thuật toán lõi.
        """
        return hash(self.board)

    def __str__(self) -> str:
        """Chuỗi hiển thị nhanh khi print(state) để debug."""
        empty_count = self.board.count(EMPTY)
        return f"SudokuState({empty_count} empty cells remaining)"